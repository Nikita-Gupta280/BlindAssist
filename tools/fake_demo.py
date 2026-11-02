# tools/fake_demo.py
import time

from alerts.alert_manager import AlertManager
from alerts.speech import Speech


def run_demo():
    manager = AlertManager()

    language = input("Choose language (en/hi): ").strip().lower()
    if language not in ("en", "hi"):
        language = "en"

    mode = input("Choose mode (quiet/normal/detailed): ").strip().lower()
    if mode not in ("quiet", "normal", "detailed"):
        mode = "normal"

    speaker = Speech(language=language)

    # Simulated detection sequence
    scenarios = [
        {
            "label": "chair",
            "id": 1,
            "conf": 0.92,
            "zone": "left",
            "dist": "medium",
            "approaching": False,
            "unknown_obstacle": False,
        },
        {
            "label": "car",
            "id": 2,
            "conf": 0.96,
            "zone": "center",
            "dist": "close",
            "approaching": True,
            "unknown_obstacle": False,
        },
        {
            "label": "person",
            "id": 3,
            "conf": 0.88,
            "zone": "right",
            "dist": "medium",
            "approaching": False,
            "unknown_obstacle": False,
        },
    ]

    try:
        print("\nStarting fake detection demo...\n")

        for detection in scenarios:
            print(f"Simulating: {detection['label']}")

            # Repeat the same detection across 5 frames
            for frame_number in range(5):
                message = manager.process(
                    detections=[detection],
                    mode=mode,
                    language=language,
                )

                if message:
                    print("ALERT:", message)
                    speaker.speak(message)

                time.sleep(0.1)

            # Pause between scenarios
            time.sleep(3.2)

        print("\nDemo completed!")

    finally:
        speaker.close()


if __name__ == "__main__":
    run_demo()
