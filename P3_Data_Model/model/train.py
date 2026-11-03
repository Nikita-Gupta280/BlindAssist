from ultralytics import YOLO

print("Loading YOLOv8n pretrained model...")

model = YOLO("yolov8n.pt")

print("Starting pothole model training...")

results = model.train(
    data="data/pothole_ready/data.yaml",
    epochs=10,
    imgsz=640,
    batch=8,
    project="runs/pothole",
    name="pothole_model",
    exist_ok=True
)

print("Training completed!")
print("Best model saved at:")
print("runs/pothole/pothole_model/weights/best.pt")