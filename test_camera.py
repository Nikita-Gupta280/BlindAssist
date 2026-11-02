
import cv2
from vision.stream import CameraStream

camera = CameraStream(0).start()

print("Camera test started. Press Q to quit.")

try:
    while True:
        frame = camera.get_frame()

        if frame is not None:
            cv2.imshow("Blind Assist", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == ord('Q'):
            break

finally:
    camera.stop()
    cv2.destroyAllWindows()
    print("Camera test stopped.")
