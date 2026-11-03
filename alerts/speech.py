# alerts/speech.py

import os
import hashlib

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import pygame
except ImportError:
    pygame = None


class Speech:
    def __init__(self, language="en"):
        self.language = language.lower()

        self.audio_folder = os.path.join(
            os.path.dirname(__file__), "audio"
        )

        self.audio_available = False

        if self.language == "hi" and pygame is not None:
            try:
                pygame.mixer.init()
                self.audio_available = True
            except Exception as e:
                print("Audio initialization failed:", e)

    def speak(self, message):
        """Speak an English alert or play a Hindi audio file."""

        if self.language == "en":

            if pyttsx3 is None:
                print("Text-to-speech is unavailable:", message)
                return

            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 155)
                engine.setProperty("volume", 1.0)
                engine.say(message)
                engine.runAndWait()
                engine.stop()
                del engine

            except Exception as e:
                print("English speech unavailable:", e)

        elif self.language == "hi":

            if not self.audio_available:
                print("Hindi audio playback unavailable:", message)
                return

            filename = self._get_hindi_filename(message)

            if os.path.exists(filename):
                try:
                    pygame.mixer.music.load(filename)
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                except Exception as e:
                    print("Hindi audio playback failed:", e)

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

        if self.audio_available:
            pygame.mixer.quit()
            self.audio_available = False
