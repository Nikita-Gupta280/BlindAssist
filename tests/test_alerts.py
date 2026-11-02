
# tests/test_alerts.py

from alerts.alert_manager import AlertManager


def make_detection(label, object_id, distance="close",
                   zone="center", approaching=False):
    return {
        "label": label,
        "id": object_id,
        "conf": 0.95,
        "zone": zone,
        "dist": distance,
        "approaching": approaching,
        "unknown_obstacle": False,
    }


def test_three_of_five_smoothing():
    manager = AlertManager()

    detection = make_detection("car", 1)

    assert manager.process([detection]) is None
    assert manager.process([detection]) is None

    alert = manager.process([detection])

    assert alert is not None
    assert "Car" in alert


def test_no_stale_alerts():
    manager = AlertManager()

    chair = make_detection("chair", 1)
    car = make_detection("car", 2, approaching=True)

    for _ in range(3):
        manager.process([chair])

    # Old chair must not be announced again
    assert manager.process([car]) is None
    assert manager.process([car]) is None

    alert = manager.process([car])

    assert alert is not None
    assert "Car" in alert


def test_priority():
    manager = AlertManager()

    chair = make_detection("chair", 1)
    car = make_detection("car", 2, approaching=True)

    for _ in range(3):
        alert = manager.process([chair, car])

    assert alert is not None
    assert "Car" in alert


def test_far_objects_are_ignored():
    manager = AlertManager()

    detection = make_detection("car", 1, distance="far")

    for _ in range(5):
        alert = manager.process([detection])

    assert alert is None


def test_quiet_mode_ignores_chairs():
    manager = AlertManager()

    chair = make_detection("chair", 1)

    for _ in range(5):
        alert = manager.process([chair], mode="quiet")

    assert alert is None


def test_cooldown():
    manager = AlertManager(cooldown=3)

    car = make_detection("car", 1)

    # First alert
    for _ in range(3):
        alert = manager.process([car])

    assert alert is not None

    # Immediate repeated alert must be suppressed
    for _ in range(5):
        alert = manager.process([car])

    assert alert is None


def test_detailed_mode():
    manager = AlertManager()

    car = make_detection("car", 1, distance="close")

    for _ in range(3):
        alert = manager.process(
            [car],
            mode="detailed"
        )

    assert alert is not None
    assert "close" in alert.lower()


def test_hindi_phrase():
    manager = AlertManager()

    car = make_detection("car", 1, approaching=True)

    for _ in range(3):
        alert = manager.process(
            [car],
            language="hi"
        )

    assert alert is not None
    assert "सावधान" in alert


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
