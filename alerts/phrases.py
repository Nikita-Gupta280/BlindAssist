
# alerts/phrases.py

# Object names used in voice alerts
OBJECT_NAMES = {
    "person": {"en": "Person", "hi": "व्यक्ति"},
    "car": {"en": "Car", "hi": "कार"},
    "motorcycle": {"en": "Motorcycle", "hi": "मोटरसाइकिल"},
    "bicycle": {"en": "Bicycle", "hi": "साइकिल"},
    "bus": {"en": "Bus", "hi": "बस"},
    "truck": {"en": "Truck", "hi": "ट्रक"},
    "chair": {"en": "Chair", "hi": "कुर्सी"},
    "dog": {"en": "Dog", "hi": "कुत्ता"},
    "bench": {"en": "Bench", "hi": "बेंच"},
    "unknown obstacle": {"en": "Obstacle", "hi": "रुकावट"},
}

# Convert detection zones into simple spoken directions
ZONE_NAMES = {
    "left": {"en": "on your left", "hi": "आपके बाईं ओर"},
    "center": {"en": "ahead", "hi": "सामने"},
    "right": {"en": "on your right", "hi": "आपके दाईं ओर"},
    "far_left": {"en": "on your far left", "hi": "आपके बिल्कुल बाईं ओर"},
    "far_right": {"en": "on your far right", "hi": "आपके बिल्कुल दाईं ओर"},
}

DISTANCE_NAMES = {
    "close": {"en": "very close", "hi": "बहुत पास"},
    "medium": {"en": "at a moderate distance", "hi": "थोड़ी दूरी पर"},
    "far": {"en": "far away", "hi": "दूर"},
}


def get_alert_phrase(label, zone, distance, language="en", detailed=False,
                     approaching=False):
    """Create a short spoken alert in English or Hindi."""

    language = language.lower()
    if language not in ("en", "hi"):
        language = "en"

    label = str(label).lower()
    zone = str(zone).lower()
    distance = str(distance).lower()

    object_name = OBJECT_NAMES.get(
        label, {"en": label.replace("_", " ").title(), "hi": "अज्ञात वस्तु"}
    )[language]

    direction = ZONE_NAMES.get(
        zone, {"en": "ahead", "hi": "सामने"}
    )[language]

    distance_text = DISTANCE_NAMES.get(
        distance, {"en": "", "hi": ""}
    )[language]

    if language == "en":
        if approaching:
            message = f"Warning! {object_name} {direction}, approaching."
        else:
            message = f"{object_name} {direction}."

        if detailed and distance_text:
            message = f"{object_name} {direction}, {distance_text}."

        return message

    if approaching:
        message = f"सावधान! {object_name} {direction} की ओर बढ़ रहा है।"
    else:
        message = f"{object_name} {direction} है।"

    if detailed and distance_text:
        message = f"{object_name} {direction} है, {distance_text}।"

    return message
