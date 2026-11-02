
import torch
from ultralytics import YOLO

from vision.logic import VisionLogic
from vision.quality import FrameQuality

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    FOCAL_PX,
    KNOWN_OBJECT_HEIGHT_CM
)


class ObjectDetector:

    def __init__(self, model_path=None):

        # Limit CPU thread usage
        torch.set_num_threads(2)

        try:
            torch.set_num_interop_threads(1)
        except RuntimeError:
            pass

        if model_path is None:
            model_path = MODEL_PATH

        self.model = YOLO(model_path)

        self.logic = VisionLogic(
            focal_px=FOCAL_PX,
            known_object_height_cm=KNOWN_OBJECT_HEIGHT_CM
        )

        self.quality = FrameQuality()

        self.latest_results = None
        self.frame_status = {}

    def detect(self, frame):

        self.frame_status = self.quality.check(frame)

        if (
            self.frame_status["blurry"]
            or self.frame_status["low_light"]
        ):
            self.latest_results = None
            return []

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=CONFIDENCE_THRESHOLD,
            imgsz=416,
            device="cpu",
            max_det=20,
            verbose=False
        )

        self.latest_results = results

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            boxes = result.boxes
            track_ids = boxes.id

            for i, box in enumerate(boxes):

                coordinates = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                label = self.model.names[class_id]

                track_id = (
                    int(track_ids[i])
                    if track_ids is not None
                    else None
                )

                zone = self.logic.get_zone(
                    coordinates,
                    frame.shape[1]
                )

                distance = self.logic.get_distance(coordinates)

                approaching = self.logic.is_approaching(
                    track_id,
                    coordinates
                )

                detections.append({
                    "label": label,
                    "id": track_id,
                    "conf": confidence,
                    "zone": zone,
                    "dist": distance,
                    "approaching": approaching,
                    "unknown_obstacle": False
                })

        return detections
