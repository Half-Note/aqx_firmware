from gpiozero import Button
import time
from picarx import Picarx  # PiCar-X motion control

# Constants
WHEEL_DIAMETER_CM = 8.65
PULSES_PER_REV = 397
DISTANCE_PER_PULSE_CM = (3.1416 * WHEEL_DIAMETER_CM) / PULSES_PER_REV

# Left wheel variables
left_position = 0
left_direction = True
left_last_a = 1

# Right wheel variables
right_position = 0
right_direction = True
right_last_a = 1

# Set up GPIO pins (adjust as needed)
right_a = Button(17, pull_up=True)
right_b = Button(4, pull_up=True)
left_a = Button(27, pull_up=True)
left_b = Button(22, pull_up=True)

# Left wheel handler (fixed)
def on_left_change():
    global left_position, left_direction, left_last_a
    new_a = left_a.value
    if left_last_a == 0 and new_a == 1:  # Detect rising edge of A
        left_direction = (left_b.value == 1)  # True=Forward, False=Backward
        left_position -= 1 if left_direction else +1  # Fixed: +1 forward, -1 backward
    left_last_a = new_a

# Right wheel handler (similar logic)
def on_right_change():
    global right_position, right_direction, right_last_a
    new_a = right_a.value
    if right_last_a == 0 and new_a == 1:  # Rising edge of A
        right_direction = (right_b.value == 1)  # True=Forward, False=Backward
        right_position += 1 if right_direction else -1  # +1 forward, -1 backward
    right_last_a = new_a

# Attach handlers
right_a.when_pressed = on_right_change
right_a.when_released = on_right_change
left_a.when_pressed = on_left_change
left_a.when_released = on_left_change

# Start PiCar-X motion test
print("Starting PiCar-X forward motion for 5 seconds...")
px = Picarx()

# Reset counters
right_position = 0
left_position = 0

px.forward(20)
time.sleep(5)
px.stop()

# Calculate distances
right_distance_cm = right_position * DISTANCE_PER_PULSE_CM
left_distance_cm = left_position * DISTANCE_PER_PULSE_CM
avg_distance_cm = (right_distance_cm + left_distance_cm) / 2

# Show results
print("\n===== 5-Second Motion Summary =====")
print(f"Right Wheel: {right_position} ticks ? {right_distance_cm:.2f} cm")
print(f"Left  Wheel: {left_position} ticks ? {left_distance_cm:.2f} cm")
print(f"Total distance traveled: {avg_distance_cm:.2f} cm")

# Optional: Keep monitoring (or comment this out)
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped")
