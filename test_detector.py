
import cv2

from vision.stream import CameraStream
from vision.detector import ObjectDetector
from config import CAMERA_SOURCE


# Start camera and detector
camera = CameraStream(CAMERA_SOURCE).start()
detector = ObjectDetector()

print("Blind Assist Vision System Started!")
print("Click on the camera window and press Q to quit.")

try:
    while True:

        frame = camera.get_frame()

        if frame is None:
            continue

        # Run object detection
        detections = detector.detect(frame)

        # Check frame quality
        status = detector.frame_status

        if status.get("low_light"):
            message = "LOW LIGHT"
            color = (0, 0, 255)

        elif status.get("blurry"):
            message = "BLURRY FRAME"
            color = (0, 0, 255)

        else:
            message = "GOOD FRAME"
            color = (0, 255, 0)

        cv2.putText(
            frame,
            message,
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        # Draw bounding boxes
        if detector.latest_results is not None:

            for result in detector.latest_results:

                if result.boxes is None:
                    continue

                for box in result.boxes:

                    x1, y1, x2, y2 = map(
                        int, box.xyxy[0].tolist()
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

        # Display detection details
        for i, obj in enumerate(detections):

            text = (
                f"{obj['label']} | "
                f"{obj['zone']} | "
                f"{obj['dist']} | "
                f"ID: {obj['id']}"
            )

            cv2.putText(
                frame,
                text,
                (20, 65 + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            print(obj)

        # Show camera window
        cv2.imshow("Blind Assist - Vision System", frame)

        # Handle exit key
        key = cv2.waitKey(1) & 0xFF

        if key in [ord('q'), ord('Q')]:
            print("Exiting Blind Assist...")
            break

        # Also exit if camera window is closed manually
        if cv2.getWindowProperty(
            "Blind Assist - Vision System",
            cv2.WND_PROP_VISIBLE
        ) < 1:
            break

finally:
    camera.stop()
    cv2.destroyAllWindows()
    print("Blind Assist Vision System Stopped.")
