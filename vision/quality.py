
import cv2

from config import BLUR_THRESHOLD, BRIGHTNESS_THRESHOLD


class FrameQuality:

    def __init__(self):

        self.blur_threshold = BLUR_THRESHOLD
        self.brightness_threshold = BRIGHTNESS_THRESHOLD

    def check(self, frame):

        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )

        brightness = float(gray.mean())

        low_light = brightness < self.brightness_threshold

        if low_light:
            blurry = False
            blur_score = 0

        else:
            blur_score = cv2.Laplacian(
                gray, cv2.CV_64F
            ).var()

            blurry = blur_score < self.blur_threshold

        return {
            "blurry": blurry,
            "low_light": low_light,
            "blur_score": round(float(blur_score), 2),
            "brightness": round(brightness, 2)
        }
