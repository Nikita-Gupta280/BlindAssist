
import cv2
import time
import queue
import threading

from vision.detector import ObjectDetector
from vision.stream import CameraStream
from alerts.alert_manager import AlertManager
from alerts.speech import Speech

from config import CAMERA_SOURCE


def speech_worker(audio_queue, speech):
    while True:
        message = audio_queue.get()

        if message is None:
            audio_queue.task_done()
            break

        try:
            speech.speak(message)
        except Exception as e:
            print("Speech error:", e)
        finally:
            audio_queue.task_done()


def main():

    print("=== BLIND ASSIST LIVE DEMO ===")

    language = input("Choose language (en/hi): ").strip().lower()
    if language not in ("en", "hi"):
        language = "en"

    mode = input("Choose mode (quiet/normal/detailed): ").strip().lower()
    if mode not in ("quiet", "normal", "detailed"):
        mode = "normal"

    camera = CameraStream(source=CAMERA_SOURCE).start()
    detector = ObjectDetector()
    alert_manager = AlertManager(cooldown=10.0)
    speech = Speech(language=language)

    audio_queue = queue.Queue(maxsize=1)

    worker = threading.Thread(
        target=speech_worker,
        args=(audio_queue, speech),
        daemon=True
    )
    worker.start()

    print("\nBlind Assist is running!")
    print("Press Q to quit.")

    try:
        while True:

            frame = camera.get_frame()

            if frame is None:
                time.sleep(0.05)
                continue

            detections = detector.detect(frame)

            message = alert_manager.process(
                detections,
                mode=mode,
                language=language
            )

            if message:
                print("ALERT:", message)

                # Don't queue duplicate alerts while speech is busy
                if audio_queue.empty():
                    audio_queue.put_nowait(message)

            display_frame = frame.copy()

            if detector.latest_results:
                display_frame = detector.latest_results[0].plot()

            status = detector.frame_status

            if status.get("blurry"):
                cv2.putText(
                    display_frame, "BLURRY FRAME",
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 255), 2
                )

            elif status.get("low_light"):
                cv2.putText(
                    display_frame, "LOW LIGHT",
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 255), 2
                )

            cv2.imshow("Blind Assist - Live Demo", display_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nStopping Blind Assist...")

    finally:
        camera.stop()

        # Finish any pending speech before closing
        audio_queue.join()
        audio_queue.put(None)
        worker.join(timeout=10)

        speech.close()
        cv2.destroyAllWindows()

        print("Blind Assist stopped.")


if __name__ == "__main__":
    main()
