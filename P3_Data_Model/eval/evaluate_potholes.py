
from ultralytics import YOLO

print("Loading trained pothole model...")

model = YOLO("model/best.pt")

print("Evaluating on test dataset...")

metrics = model.val(
    data="data/pothole_ready/data.yaml",
    split="test",
    imgsz=640,
    batch=4
)

print("\nFINAL TEST RESULTS")
print("Precision:", metrics.box.mp)
print("Recall:", metrics.box.mr)
print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)

print("\nEvaluation completed!")
