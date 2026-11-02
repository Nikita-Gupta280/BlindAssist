
def check_free_space(detections, image_width, image_height):
    """
    Identifies candidate unoccupied regions in an image.

    This is a basic experimental heuristic, NOT a safe-path
    detector. No detection does not mean the path is safe.
    """

    left_clear = True
    center_clear = True
    right_clear = True

    for detection in detections:
        x1, y1, x2, y2 = detection

        center_x = (x1 + x2) / 2

        if center_x < image_width / 3:
            left_clear = False
        elif center_x < 2 * image_width / 3:
            center_clear = False
        else:
            right_clear = False

    return {
        "left_candidate_clear": left_clear,
        "center_candidate_clear": center_clear,
        "right_candidate_clear": right_clear
    }


if __name__ == "__main__":
    # Example test using imaginary bounding boxes
    sample_detections = [
        (50, 100, 200, 400),
        (450, 150, 600, 450)
    ]

    result = check_free_space(
        sample_detections,
        image_width=640,
        image_height=480
    )

    print("Experimental image-region analysis:")
    print(result)
