
from ultralytics import YOLO

print("Loading trained door model...")

model = YOLO("model/best_doors.pt")

print("Evaluating on door test dataset...")

metrics = model.val(
    data="data/doors_ready/data.yaml",
    split="test",
    imgsz=640,
    batch=4
)

print("\nFINAL DOOR TEST RESULTS")
print("Precision:", metrics.box.mp)
print("Recall:", metrics.box.mr)
print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)

print("\nDoor evaluation completed!")
