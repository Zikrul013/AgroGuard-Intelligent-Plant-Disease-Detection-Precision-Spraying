from ultralytics import YOLO

# 1. Load YOUR custom-trained brain from the train4 folder
model = YOLO(r"D:\tomato\runs\detect\train4\weights\best.pt")

# 2. Tell the model to look at your test image
# (Make sure 'test_image.jpg' is the exact name of your picture)
results = model.predict(source="test_image.jpg", show=True, save=True)

print("Test complete! The AI has made its predictions.")