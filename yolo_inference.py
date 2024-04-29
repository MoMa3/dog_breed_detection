from ultralytics import YOLO

model = YOLO("models/best.pt")
model.predict(
    "input_pictures/download (1).jpeg",
    save=True,
)
