
from ultralytics import YOLO

print("Loading YOLOv8n pretrained model...")

model = YOLO("yolov8n.pt")

print("Starting door detection training...")

results = model.train(
    data="data/doors_ready/data.yaml",
    epochs=10,
    imgsz=640,
    batch=8,
    project="runs/doors",
    name="doors_model",
    exist_ok=True
)

print("Door training completed!")
print("Best model saved in runs/doors/doors_model/weights/best.pt")
