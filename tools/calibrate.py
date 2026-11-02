
import cv2

# Enter the actual height of the object and its distance
object_height_cm = float(input("Actual object height (cm): "))
distance_cm = float(input("Distance from camera (cm): "))

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open camera.")
    exit()

print("Place the object at the measured distance.")
print("Press SPACE to select the object, then ENTER.")

while True:
    success, frame = cap.read()

    if not success:
        print("Could not read camera.")
        break

    cv2.imshow("Calibration", frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        cap.release()
        cv2.destroyAllWindows()

        roi = cv2.selectROI("Select Object", frame, False)
        cv2.destroyAllWindows()

        x, y, width, height = roi

        if height == 0:
            print("Invalid selection.")
            exit()

        focal_length = (height * distance_cm) / object_height_cm

        print("\nCalibration complete!")
        print("Measured bounding box height:", height, "pixels")
        print("FOCAL_PX =", round(focal_length, 2))

        break

cap.release()
cv2.destroyAllWindows()
