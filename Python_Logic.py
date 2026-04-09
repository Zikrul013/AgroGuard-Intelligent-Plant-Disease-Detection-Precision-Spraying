import math

# --- PHYSICAL PROTOTYPE CONSTANTS ---
GARDEN_WIDTH_X = 30.0  # cm (Rail length)
GARDEN_DEPTH_Y = 40.0  # cm (Targeting depth)
NOZZLE_HEIGHT_Z = 25.0  # cm (Height from the ground)
NOZZLE_OFFSET_Y = 2.0  # cm (Distance nozzle tip sticks out from the carriage center)

# The "Geometric Cone" from your animation
SPRAY_SPREAD_ANGLE = 15.0  # Degrees (Total width of the spray cone)


def calculate_targeting(plant_x, plant_y):
    """
    Calculates the required X carriage position and Y servo tilt angle
    to hit a specific plant coordinate.
    """
    # 1. X-Axis: Carriage moves directly over the plant's X coordinate
    carriage_x = plant_x

    # Constrain carriage to the physical 30cm rail
    carriage_x = max(0.0, min(GARDEN_WIDTH_X, carriage_x))

    # 2. Y-Axis: Calculate the horizontal distance the spray needs to travel
    # We subtract the offset because the nozzle sticks out slightly from the rail
    target_distance_y = plant_y - NOZZLE_OFFSET_Y

    # Prevent negative targeting (if plant is somehow behind the rail)
    target_distance_y = max(0.0, target_distance_y)

    # Calculate the tilt angle using Arctangent (Opposite / Adjacent)
    # math.atan2 returns radians, so we convert it to degrees
    tilt_angle_rad = math.atan2(target_distance_y, NOZZLE_HEIGHT_Z)
    tilt_angle_deg = math.degrees(tilt_angle_rad)

    return carriage_x, tilt_angle_deg


def is_plant_in_spray_cone(plant_x, plant_y, current_carriage_x, current_tilt_angle):
    """
    Validates if the plant actually falls inside the "Geometric Cone"
    before triggering the pump.
    """
    # Check X alignment (is the carriage directly in front of the plant?)
    # Let's say we have a 2cm margin of error for the spray width on the X-axis
    if abs(plant_x - current_carriage_x) > 2.0:
        return False, "Carriage X-Axis not aligned."

    # Calculate the exact angle required to hit the plant
    _, required_tilt = calculate_targeting(plant_x, plant_y)

    # Check Y alignment (is the servo tilted correctly?)
    # We check if the current angle is within half of the spray cone's spread
    half_cone = SPRAY_SPREAD_ANGLE / 2.0

    if abs(required_tilt - current_tilt_angle) <= half_cone:
        return True, "Target Locked. Ready to Spray!"
    else:
        return False, "Tilt Y-Axis not aligned."


# ==========================================
# --- TEST SIMULATION based on Prototype ---
# ==========================================
if __name__ == "__main__":
    print("--- 30x40 cm Garden Prototype Simulation ---")

    # Example: YOLO detects an infected plant at X=15cm, Y=20cm
    infected_plant_x = 15.0
    infected_plant_y = 20.0

    print(f"\nInfected Plant Detected at: X={infected_plant_x}cm, Y={infected_plant_y}cm")

    # 1. Calculate Movements
    target_x, target_tilt = calculate_targeting(infected_plant_x, infected_plant_y)

    print(f"-> Moving Carriage (X) to: {target_x:.1f} cm")
    # For a standard 180 servo, 0 degrees is straight down.
    print(f"-> Tilting Nozzle (Y) to: {target_tilt:.1f} degrees from vertical")

    # 2. Verify Cone
    # Simulate the servos finishing their movement
    current_x = target_x
    current_angle = target_tilt

    locked, message = is_plant_in_spray_cone(infected_plant_x, infected_plant_y, current_x, current_angle)
    print(f"\nStatus: {message}")