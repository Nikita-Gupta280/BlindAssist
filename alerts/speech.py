
# alerts/speech.py

import os
import hashlib
import pyttsx3
import pygame


class Speech:
    def __init__(self, language="en"):
        self.language = language.lower()

        self.audio_folder = os.path.join(
            os.path.dirname(__file__), "audio"
        )

        # Initialise Hindi audio playback
        if self.language == "hi":
            pygame.mixer.init()

    def speak(self, message):
        """Speak an English alert or play a Hindi audio file."""

        if self.language == "en":

            # Create a fresh engine for every message
            engine = pyttsx3.init()
            engine.setProperty("rate", 155)
            engine.setProperty("volume", 1.0)

            engine.say(message)
            engine.runAndWait()
            engine.stop()

            del engine

        elif self.language == "hi":

            filename = self._get_hindi_filename(message)

            if os.path.exists(filename):
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

            else:
                print("Hindi audio not found:", message)

    def _get_hindi_filename(self, message):
        filename = hashlib.md5(
            message.encode("utf-8")
        ).hexdigest()

        return os.path.join(
            self.audio_folder, filename + ".mp3"
        )

    def close(self):
        """Release audio resources."""

        if self.language == "hi":
            pygame.mixer.quit()
