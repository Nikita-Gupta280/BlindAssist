
# alerts/pregenerate_hindi.py

import os
import hashlib
from gtts import gTTS

from alerts.phrases import get_alert_phrase


AUDIO_FOLDER = os.path.join(
    os.path.dirname(__file__), "audio"
)

LABELS = [
    "person", "car", "motorcycle", "bicycle",
    "bus", "truck", "chair", "dog", "bench",
    "unknown obstacle"
]

ZONES = ["left", "center", "right", "far_left", "far_right"]

DISTANCES = ["close", "medium"]


def get_filename(message):
    filename = hashlib.md5(message.encode("utf-8")).hexdigest()
    return os.path.join(AUDIO_FOLDER, filename + ".mp3")


def generate_hindi_audio():
    os.makedirs(AUDIO_FOLDER, exist_ok=True)

    messages = set()

    # Generate normal and detailed alert phrases
    for label in LABELS:
        for zone in ZONES:
            for distance in DISTANCES:
                for detailed in [False, True]:
                    for approaching in [False, True]:

                        message = get_alert_phrase(
                            label=label,
                            zone=zone,
                            distance=distance,
                            language="hi",
                            detailed=detailed,
                            approaching=approaching
                        )

                        messages.add(message)

    print(f"Generating {len(messages)} Hindi audio files...")

    for index, message in enumerate(sorted(messages), start=1):
        filename = get_filename(message)

        if os.path.exists(filename):
            continue

        try:
            audio = gTTS(text=message, lang="hi")
            audio.save(filename)
            print(f"{index}/{len(messages)} Generated: {message}")

        except Exception as error:
            print(f"Failed: {message}")
            print(error)

    print("Hindi audio generation completed!")


if __name__ == "__main__":
    generate_hindi_audio()
