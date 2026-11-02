
import cv2
from vision.stream import CameraStream
from vision.quality import FrameQuality

camera = CameraStream(0).start()
quality = FrameQuality()

while True:

    frame = camera.get_frame()

    if frame is None:
        continue

    result = quality.check(frame)

    print(result)

    status = []

    if result["blurry"]:
        status.append("BLURRY")

    if result["low_light"]:
        status.append("LOW LIGHT")

    message = " | ".join(status) if status else "GOOD FRAME"

    cv2.putText(
        frame, message, (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
        (0, 0, 255) if status else (0, 255, 0), 2
    )

    cv2.imshow("Frame Quality Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
cv2.destroyAllWindows()
