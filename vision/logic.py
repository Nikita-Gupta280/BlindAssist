
from config import (
    CLOSE_DISTANCE,
    MEDIUM_DISTANCE,
    APPROACHING_THRESHOLD
)


class VisionLogic:

    def __init__(self, focal_px, known_object_height_cm):
        self.focal_px = focal_px
        self.known_object_height_cm = known_object_height_cm
        self.previous_heights = {}

    def get_zone(self, box, frame_width):

        x1, y1, x2, y2 = box
        center_x = (x1 + x2) / 2
        position = center_x / frame_width

        if position < 0.2:
            return "far-left"
        elif position < 0.4:
            return "left"
        elif position < 0.6:
            return "center"
        elif position < 0.8:
            return "right"
        else:
            return "far-right"

    def get_distance(self, box):

        x1, y1, x2, y2 = box
        height = y2 - y1

        if height <= 0:
            return None

        distance_cm = (
            self.known_object_height_cm * self.focal_px
        ) / height

        if distance_cm < CLOSE_DISTANCE:
            return "close"
        elif distance_cm < MEDIUM_DISTANCE:
            return "medium"
        else:
            return "far"

    def is_approaching(self, track_id, box):

        if track_id is None:
            return False

        x1, y1, x2, y2 = box
        current_height = y2 - y1

        previous_height = self.previous_heights.get(track_id)
        self.previous_heights[track_id] = current_height

        if previous_height is None or previous_height <= 0:
            return False

        growth = current_height / previous_height

        return growth > APPROACHING_THRESHOLD
