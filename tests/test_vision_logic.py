import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))



from vision.logic import VisionLogic

logic = VisionLogic(
    focal_px=420.5,
    known_object_height_cm=30
)

def check(name, condition):
    if condition:
        print(f"PASS: {name}")
    else:
        print(f"FAIL: {name}")


# Test 1: Zone detection
check(
    "Far-left zone",
    logic.get_zone([0, 0, 100, 100], 500) == "far-left"
)

check(
    "Center zone",
    logic.get_zone([200, 0, 300, 100], 500) == "center"
)

check(
    "Far-right zone",
    logic.get_zone([400, 0, 500, 100], 500) == "far-right"
)


# Test 2: Distance detection
check(
    "Close distance",
    logic.get_distance([0, 0, 100, 200]) == "close"
)

check(
    "Medium distance",
    logic.get_distance([0, 0, 100, 50]) == "medium"
)

check(
    "Far distance",
    logic.get_distance([0, 0, 100, 20]) == "far"
)


# Test 3: Approaching detection
track_id = 1

logic.previous_heights.clear()

check(
    "First observation",
    logic.is_approaching(track_id, [0, 0, 100, 100]) == False
)

check(
    "Object approaching",
    logic.is_approaching(track_id, [0, 0, 100, 120]) == True
)
