
# alerts/alert_manager.py

from collections import deque
from time import monotonic

from alerts.phrases import get_alert_phrase


class AlertManager:
    def __init__(self, cooldown=10.0, window_size=5, min_detections=3):
        self.cooldown = cooldown
        self.min_detections = min_detections

        # Store detections from the last 5 frames
        self.history = deque(maxlen=window_size)

        # Store the last alert time for each tracked object
        self.last_alert_time = {}

        # Lower number means higher priority
        self.priority = {
            "car": 1,
            "truck": 2,
            "bus": 3,
            "motorcycle": 4,
            "bicycle": 5,
            "person": 6,
            "dog": 7,
            "unknown obstacle": 8,
            "chair": 9,
            "bench": 10,
        }

    def _get_object_key(self, detection):
        """Identify an object across multiple frames."""

        label = str(
            detection.get("label", "unknown obstacle")
        ).lower()

        if detection.get("unknown_obstacle", False):
            label = "unknown obstacle"

        object_id = detection.get("id")

        if object_id is not None:
            return (label, object_id)

        # Fallback when tracking ID is unavailable
        return (label, detection.get("zone", "center"))

    def process(self, detections, mode="normal", language="en"):
        """
        Process detections from one frame.

        Returns one alert message or None.
        """

        mode = mode.lower()

        if mode not in ("quiet", "normal", "detailed"):
            mode = "normal"

        # Prepare detections from the current frame
        current_frame = {}

        for detection in detections:

            label = str(
                detection.get("label", "unknown obstacle")
            ).lower()

            if detection.get("unknown_obstacle", False):
                label = "unknown obstacle"

            distance = str(
                detection.get("dist", "far")
            ).lower()

            # Ignore faraway objects
            if distance == "far":
                continue

            # Quiet mode ignores chairs and benches
            if mode == "quiet" and label in ("chair", "bench"):
                continue

            key = self._get_object_key(detection)
            current_frame[key] = detection

        # Add current frame to history
        self.history.append(current_frame)

        # Count appearances in the last 5 frames
        counts = {}

        for frame in self.history:
            for key in frame:
                counts[key] = counts.get(key, 0) + 1

        # Only consider objects that:
        # 1. Appeared in at least 3 of the last 5 frames
        # 2. Are still present in the current frame
        candidates = []

        for key, count in counts.items():
            if count >= self.min_detections and key in current_frame:
                candidates.append(current_frame[key])

        # Sort candidates by priority
        candidates.sort(
            key=lambda detection: self.priority.get(
                "unknown obstacle"
                if detection.get("unknown_obstacle", False)
                else str(
                    detection.get("label", "")
                ).lower(),
                99
            )
        )

        current_time = monotonic()

        # Return only one alert per frame
        for detection in candidates:

            key = self._get_object_key(detection)

            # Check cooldown
            last_time = self.last_alert_time.get(key, 0)

            if current_time - last_time < self.cooldown:
                continue

            label = (
                "unknown obstacle"
                if detection.get("unknown_obstacle", False)
                else str(
                    detection.get("label", "unknown obstacle")
                ).lower()
            )

            # Generate the spoken message
            message = get_alert_phrase(
                label=label,
                zone=detection.get("zone", "center"),
                distance=detection.get("dist", "far"),
                language=language,
                detailed=(mode == "detailed"),
                approaching=detection.get("approaching", False)
            )

            self.last_alert_time[key] = current_time

            return message

        return None

