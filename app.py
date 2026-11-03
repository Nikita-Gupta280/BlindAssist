
import streamlit as st
import cv2
import time
import queue
import threading

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

from vision.detector import ObjectDetector
from vision.stream import CameraStream
from alerts.alert_manager import AlertManager
from alerts.speech import Speech
from config import CAMERA_SOURCE


st.set_page_config(
    page_title="Blind Assist",
    page_icon="👁️",
    layout="wide"
)


# --------------------------------
# Shared runtime state
# --------------------------------

if "runtime" not in st.session_state:

    st.session_state.runtime = {
        "running": False,
        "thread": None,
        "stop_event": None,
        "lock": threading.Lock(),
        "frame": None,
        "detections": [],
        "alert": None,
        "status": "Stopped",
        "error": None,
        "language": "en",
        "mode": "normal",
    }


runtime = st.session_state.runtime
# --------------------------------
# Browser camera processor
# --------------------------------

class CameraProcessor(VideoProcessorBase):

    def __init__(self, runtime, audio_queue):
        self.runtime = runtime
        self.audio_queue = audio_queue

        self.detector = ObjectDetector()
        self.alert_manager = AlertManager(cooldown=10.0)
        self.frame_count = 0

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1

        if self.frame_count % 2 == 0:

            with self.runtime["lock"]:
                language = self.runtime["language"]
                mode = self.runtime["mode"]

            detections = self.detector.detect(img)

            message = self.alert_manager.process(
                detections,
                mode=mode,
                language=language
            )

            if message:
                with self.runtime["lock"]:
                    self.runtime["alert"] = message

                if self.audio_queue.empty():
                    self.audio_queue.put_nowait(
                        (message, language)
                    )

            display_frame = img.copy()

            if self.detector.latest_results:
                display_frame = self.detector.latest_results[0].plot()

            with self.runtime["lock"]:
                self.runtime["detections"] = detections
                self.runtime["frame"] = cv2.cvtColor(
                    display_frame,
                    cv2.COLOR_BGR2RGB
                )
                self.runtime["status"] = "Running"

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


# --------------------------------
# Speech worker
# --------------------------------

def speech_worker(audio_queue):

    speech = None
    current_language = None

    try:

        while True:

            item = audio_queue.get()

            try:

                if item is None:
                    break

                message, language = item

                if language != current_language:

                    if speech:
                        speech.close()

                    speech = Speech(language=language)
                    current_language = language

                speech.speak(message)

            finally:
                audio_queue.task_done()

    except Exception as e:
        print("Speech error:", e)

    finally:

        if speech:
            speech.close()


# --------------------------------
# Vision worker
# --------------------------------

# --------------------------------
# Shared audio queue
# --------------------------------

if "audio_queue" not in st.session_state:
    st.session_state.audio_queue = queue.Queue(maxsize=1)

audio_queue = st.session_state.audio_queue
if "speech_thread" not in st.session_state:
    st.session_state.speech_thread = threading.Thread(
        target=speech_worker,
        args=(audio_queue,),
        daemon=True
    )
    st.session_state.speech_thread.start()

def vision_worker(runtime, stop_event, audio_queue):

    camera = CameraStream(source=CAMERA_SOURCE).start()

    try:

        detector = ObjectDetector()

        alert_manager = AlertManager(cooldown=10.0)

        frame_count = 0

        with runtime["lock"]:
            runtime["status"] = "Camera starting..."

        while not stop_event.is_set():

            frame = camera.get_frame()

            if frame is None:
                time.sleep(0.05)
                continue

            # Process every second frame
            frame_count += 1

            if frame_count % 2 != 0:
                continue

            # Object detection
            detections = detector.detect(frame)

            # Read latest settings
            with runtime["lock"]:

                current_language = runtime["language"]
                current_mode = runtime["mode"]

            # Generate alert
            message = alert_manager.process(
                detections,
                mode=current_mode,
                language=current_language
            )

            if message:

                with runtime["lock"]:
                    runtime["alert"] = message

                if audio_queue.empty():
                    audio_queue.put_nowait(
                        (message, current_language)
                    )

            # Draw detection boxes
            display_frame = frame.copy()

            if detector.latest_results:
                display_frame = detector.latest_results[0].plot()

            display_frame = cv2.cvtColor(
                display_frame,
                cv2.COLOR_BGR2RGB
            )

            # Update dashboard
            with runtime["lock"]:

                runtime["frame"] = display_frame
                runtime["detections"] = detections
                runtime["status"] = "Running"

    except Exception as e:

        with runtime["lock"]:

            runtime["error"] = str(e)
            runtime["status"] = "Error"

        print("Vision worker error:", e)

    finally:

        camera.stop()

        audio_queue.join()
        audio_queue.put(None)

        with runtime["lock"]:

            runtime["running"] = False

            if runtime["status"] != "Error":
                runtime["status"] = "Stopped"


# --------------------------------
# Start detection
# --------------------------------

def start_detection(runtime):

    with runtime["lock"]:

        if runtime["running"]:
            return

        runtime["frame"] = None
        runtime["detections"] = []
        runtime["alert"] = None
        runtime["error"] = None
        runtime["status"] = "Starting..."
        runtime["running"] = True

        stop_event = threading.Event()

        runtime["stop_event"] = stop_event

    audio_queue = queue.Queue(maxsize=1)

    speech_thread = threading.Thread(
        target=speech_worker,
        args=(audio_queue,),
        daemon=True
    )

    speech_thread.start()

    vision_thread = threading.Thread(
        target=vision_worker,
        args=(runtime, stop_event, audio_queue),
        daemon=True
    )

    runtime["thread"] = vision_thread

    vision_thread.start()


# --------------------------------
# Stop detection
# --------------------------------

def stop_detection(runtime):

    with runtime["lock"]:

        if runtime["running"] and runtime["stop_event"]:

            runtime["status"] = "Stopping..."
            runtime["stop_event"].set()


# --------------------------------
# Dashboard
# --------------------------------

st.title("👁️ Blind Assist")

st.caption(
    "AI-powered visual assistance for visually impaired users"
)

st.divider()


# --------------------------------
# Sidebar settings
# --------------------------------

st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Voice language",
    ["English", "Hindi"],
    key="language_setting"
)

mode = st.sidebar.selectbox(
    "Alert mode",
    ["Normal", "Quiet", "Detailed"],
    key="mode_setting"
)

with runtime["lock"]:

    runtime["language"] = (
        "en" if language == "English" else "hi"
    )

    runtime["mode"] = mode.lower()


# --------------------------------
# WebRTC live camera
# --------------------------------

st.subheader("Live Camera")

ctx = webrtc_streamer(
    key="blindassist-camera",
    video_processor_factory=lambda: CameraProcessor(
        runtime,
        audio_queue
    ),
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]}
        ]
    },
)

if ctx.state.playing:
    st.success("Live camera connected")
else:
    st.info("Click START to activate your laptop camera.")

st.divider()


# --------------------------------
# Live dashboard
# --------------------------------

@st.fragment(run_every=0.7)
def live_dashboard():

    with runtime["lock"]:

        frame = runtime["frame"]
        detections = list(runtime["detections"])
        alert = runtime["alert"]
        status = runtime["status"]
        error = runtime["error"]

    camera_col, info_col = st.columns([2, 1])

    with camera_col:

        st.subheader("Live Camera Feed")

        if frame is not None:

            st.image(
                frame,
                channels="RGB",
                use_container_width=True
            )

        else:

            st.info(
                "Camera feed will appear here after starting detection."
            )


    with info_col:

        st.subheader("System Status")

        st.write(
            "Camera / detection:",
            status
        )

        st.subheader("Latest Voice Alert")

        if alert:
            st.warning(alert)

        else:
            st.write("No alerts yet.")


        st.subheader("Detected Objects")

        if detections:

            rows = [

                {
                    "Object": d["label"],
                    "Zone": d["zone"],
                    "Distance": d["dist"],
                    "Approaching": (
                        "Yes" if d["approaching"] else "No"
                    )
                }

                for d in detections

            ]

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.write("No objects currently detected.")


        if error:
            st.error(error)


live_dashboard()
