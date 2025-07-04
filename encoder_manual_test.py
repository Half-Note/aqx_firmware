from gpiozero import Button
import time

# Constants
WHEEL_DIAMETER_CM = 6.8 #wheel dia 6.8 but to config the actual distance its 8.65
PULSES_PER_REV = 397
DISTANCE_PER_PULSE_CM = (3.1416 * WHEEL_DIAMETER_CM) / PULSES_PER_REV 

# Left wheel variables
left_position = 0
left_direction = True
left_last_a = 1
left_distance_cm = 0.0

# Right wheel variables
right_position = 0
right_direction = True
right_last_a = 1
right_distance_cm = 0.0

# Set up GPIO pins (adjust as needed)
# Right encoder: A = GPIO17 (D0), B = GPIO4 (D1)
right_a = Button(17, pull_up=True)
right_b = Button(4, pull_up=True)

# Left encoder: A = GPIO27 (D3), B = GPIO22 (D2)
left_a = Button(27, pull_up=True)
left_b = Button(22, pull_up=True)

# Right wheel handler
def on_right_change():
    global right_position, right_direction, right_last_a, right_distance_cm
    new_a = right_a.value
    if right_last_a == 0 and new_a == 1:  # rising edge
        right_direction = True if right_b.value == 1 else False
        right_position += 1 if right_direction else -1
        right_distance_cm = right_position * DISTANCE_PER_PULSE_CM
        print(f"[Right] Direction: {'Forward' if right_direction else 'Backward'}, Position: {right_position}, Distance: {right_distance_cm:.3f} cm")
    right_last_a = new_a

# Left wheel handler
def on_left_change():
    global left_position, left_direction, left_last_a, left_distance_cm
    new_a = left_a.value
    if left_last_a == 0 and new_a == 1:  # rising edge
        left_direction = True if left_b.value == 1 else False
        left_position += 1 if left_direction else -1
        left_distance_cm = left_position * DISTANCE_PER_PULSE_CM
        print(f"[Left]  Direction: {'Forward' if left_direction else 'Backward'}, Position: {left_position}, Distance: {left_distance_cm:.3f} cm")
    left_last_a = new_a

# Attach interrupt handlers
right_a.when_pressed = on_right_change
right_a.when_released = on_right_change

left_a.when_pressed = on_left_change
left_a.when_released = on_left_change

print("Rotate encoders manually")

try:
    while True:
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Stopped")