# --- CAMERA & GARDEN CONSTANTS ---
# Standard YOLO/OpenCV camera resolution
CAMERA_WIDTH_PX = 640.0
CAMERA_HEIGHT_PX = 480.0

# Your physical prototype dimensions
GARDEN_WIDTH_CM = 30.0
GARDEN_DEPTH_CM = 40.0


def yolo_to_physical_coordinates(bounding_box):
    """
    Converts a YOLO bounding box (pixels) into physical target coordinates (cm).
    bounding_box format: (x_min, y_min, x_max, y_max)
    """
    x_min, y_min, x_max, y_max = bounding_box

    # Step 1: Find the exact center of the detected plant in pixels
    center_x_px = (x_min + x_max) / 2.0
    center_y_px = (y_min + y_max) / 2.0

    # Step 2: Convert the pixel location into a percentage (0.0 to 1.0)
    # Example: If center is at pixel 320 on a 640 wide image, percent is 0.5 (50%)
    percent_x = center_x_px / CAMERA_WIDTH_PX
    percent_y = center_y_px / CAMERA_HEIGHT_PX

    # Step 3: Apply the percentage to your physical garden dimensions
    target_x_cm = percent_x * GARDEN_WIDTH_CM

    # NOTE: In computer vision, Y=0 is the TOP of the image.
    # If the TOP of your camera view is the BACK of your garden (40cm mark),
    # we calculate it straight. If it's reversed, you would do: (1.0 - percent_y) * GARDEN_DEPTH_CM
    target_y_cm = percent_y * GARDEN_DEPTH_CM

    return target_x_cm, target_y_cm


# ==========================================
# --- SIMULATING THE FULL PIPELINE ---
# ==========================================
if __name__ == "__main__":
    print("--- AI to Physical Mapping Test ---")

    # Example: YOLO detects an infected tomato plant bounding box
    # Let's say it's on the right side, about halfway deep.
    yolo_bbox = (400, 200, 480, 280)  # (x_min, y_min, x_max, y_max)

    print(f"1. AI Detected Bounding Box (Pixels): {yolo_bbox}")

    # Run the conversion
    plant_cm_x, plant_cm_y = yolo_to_physical_coordinates(yolo_bbox)

    print(f"2. Converted Physical Location: X = {plant_cm_x:.1f} cm, Y = {plant_cm_y:.1f} cm")

    # Now, pass these CM values into the targeting function from the PREVIOUS code!
    # target_x, target_tilt = calculate_targeting(plant_cm_x, plant_cm_y)
    print("\nSuccess! These CM values can now be sent to the Servos.")