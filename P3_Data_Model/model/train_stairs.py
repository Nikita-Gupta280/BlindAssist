
from ultralytics import YOLO

print("Loading YOLOv8n pretrained model...")

model = YOLO("yolov8n.pt")

print("Starting stairs detection training...")

results = model.train(
    data="data/stairs_ready/data.yaml",
    epochs=10,
    imgsz=640,
    batch=8,
    project="runs/stairs",
    name="stairs_model",
    exist_ok=True
)

print("Stairs training completed!")
print("Best model will be saved in:")
print("runs/stairs/stairs_model/weights/best.pt")
