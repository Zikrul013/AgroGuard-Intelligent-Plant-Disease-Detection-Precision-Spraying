import cv2
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from gpiozero import OutputDevice
from ultralytics import YOLO
from picamera2 import Picamera2
from flask import Flask, Response

# ==========================================
# 1. INITIALIZATION & HARDWARE SETUP
# ==========================================
app = Flask(__name__)

print("--- Initializing Hardware ---")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50

    # Servos on Channel 0 (Pan) and Channel 15 (Tilt)
    pan_servo = servo.Servo(pca.channels[0])
    tilt_servo = servo.Servo(pca.channels[15])

    # Water Pump Relay on GPIO 17
    pump_relay = OutputDevice(17, active_high=False, initial_value=True)
    print("Hardware Ready.")
except Exception as e:
    print(f"Hardware Error: {e}")
    print("Check your I2C wiring!")

print("--- Loading AI Model ---")
model = YOLO('best.pt')

print("--- Starting Camera ---")
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()


# ==========================================
# 2. CORE LOGIC & AI LOOP
# ==========================================
def generate_frames():
    last_spray_time = 0  # স্প্রে করার সময় মনে রাখার জন্য

    while True:
        # 1. Capture Frame
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 2. Run AI Inference
        results = model.predict(source=frame, conf=0.5, show=False, verbose=False)

        for result in results:
            for box in result.boxes:
                # Get center coordinates of the target
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

                # Extract Disease Name
                cls_id = int(box.cls[0].cpu().numpy())
                disease_name = model.names[cls_id].upper()

                # --- INDEPENDENT EDGE CALIBRATION (YOUR PERFECTED VALUES) ---
                PAN_LEFT_EDGE = 140
                PAN_RIGHT_EDGE = 68

                TILT_TOP_EDGE = 125
                TILT_BOTTOM_EDGE = 45

                # Dynamically map the pixel coordinates to your specific hardware edges
                pan_angle = PAN_LEFT_EDGE + ((cx / 640.0) * (PAN_RIGHT_EDGE - PAN_LEFT_EDGE))
                tilt_angle = TILT_TOP_EDGE + ((cy / 480.0) * (TILT_BOTTOM_EDGE - TILT_TOP_EDGE))

                # Apply limits safely (Clamps the servo strictly between your custom edge variables)
                pan_servo.angle = max(PAN_RIGHT_EDGE, min(PAN_LEFT_EDGE, pan_angle))
                tilt_servo.angle = max(TILT_BOTTOM_EDGE, min(TILT_TOP_EDGE, tilt_angle))

                print(f"[{disease_name}] at ({cx},{cy}) -> Moving: Pan {pan_angle:.1f}°, Tilt {tilt_angle:.1f}°")

                # 3. Visuals for the stream
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"{disease_name} DETECTED", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                # ==========================================
                # 4. SMART PUMP CONTROL (WITH COOLDOWN)
                # ==========================================
                current_time = time.time()

                # ৩ সেকেন্ডের Cooldown চেক
                if current_time - last_spray_time > 3.0:
                    print("💦 PUMP ACTIVATED - SPRAYING!")
                    pump_relay.on()
                    time.sleep(0.5)  # পাম্পটি ০.৫ সেকেন্ড স্প্রে করবে
                    pump_relay.off()
                    last_spray_time = time.time()
                else:
                    pump_relay.off()

        # 5. Encode and Send to Web/ffplay
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


# 3. WEB SERVER SETUP
# ==========================================
@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    try:
        print("🌐 Stream starting at http://0.0.0.0:5000")
        print("💻 On Windows, run: ffplay -i http://192.168.137.199:5000")
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        print("\nShutting down hardware...")
        picam2.stop()
        pump_relay.off()