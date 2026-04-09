from ultralytics import YOLO

# 1. Load your custom-trained "brain"
model = YOLO(r"D:\tomato\runs\detect\train4\weights\best.pt")

print("Starting webcam... Press 'q' inside the video window to stop.")

# 2. Start the live video feed!
# source=0 means "use the default webcam"
# show=True opens the window to see the boxes
model.predict(source=0, show=True, conf=0.5)