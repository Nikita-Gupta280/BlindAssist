from pathlib import Path

from ultralytics import YOLO
from vision.logic import VisionLogic
from config import FOCAL_PX, KNOWN_OBJECT_HEIGHT_CM


class P3HazardDetector:
    """Experimental P3 detector for potholes, stairs and doors."""

    def __init__(self):
        base = Path(__file__).resolve().parent / "model"

        self.models = {
            "pothole": YOLO(str(base / "best_pothole.pt")),
            "stairs": YOLO(str(base / "best_stairs.pt")),
            "doors": YOLO(str(base / "best_doors.pt")),
        }

        self.logic = VisionLogic(
            focal_px=FOCAL_PX,
            known_object_height_cm=KNOWN_OBJECT_HEIGHT_CM
        )

    def detect(self, frame):
        detections = []

        for model_name, model in self.models.items():
            results = model.predict(
                frame,
                conf=0.25,
                imgsz=416,
                device="cpu",
                verbose=False
            )

            for result in results:
                if result.boxes is None:
                    continue

                for box in result.boxes:
                    coordinates = box.xyxy[0].tolist()
                    class_id = int(box.cls[0])
                    label = str(model.names[class_id])

                    zone = self.logic.get_zone(
                        coordinates, frame.shape[1]
                    )
                    distance = self.logic.get_distance(coordinates)

                    detections.append({
                        "label": label,
                        "id": None,
                        "conf": float(box.conf[0]),
                        "zone": zone,
                        "dist": distance,
                        "approaching": False,
                        "unknown_obstacle": False,
                        "model": model_name,
                        "experimental": True
                    })

        return detections
