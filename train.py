from ultralytics import YOLO

def main():
    model = YOLO("yolo11n.pt")

    model.train(
        data="Tomato-Leaf-Disease-6/data.yaml",
        epochs=25,
        imgsz=640,
        device=0,
        batch=8,       # Lowered slightly for extra safety
        workers=0,     # 0 completely prevents Windows memory crashes
        amp=False      # <--- THE MAGIC FIX: Turns off buggy mixed-precision math
    )

if __name__ == '__main__':
    main()