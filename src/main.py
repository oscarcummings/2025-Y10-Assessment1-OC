from machine import Pin, PWM
from servo import Servo
from ultrasonic import Ultrasonic
from encoded_motor import Motor
from time import sleep_ms, ticks_ms

ROTATION = 22  # cm
## Your implementation goes here
# Servo = GPIO28
# Ultrasonic = { Echo: GPIO20, Trigger: GPIO21 }
# Left Motor = { Forward: 14, Reverse: 15, Speed: 13, Encoder : 3 }
# Right Motor = { Forward: 17, Reverse: 16, Speed: 18, Encoder : 4 }

left_motor = Motor(14, 15, 13, 3)
right_motor = Motor(17, 16, 18, 4)

left_motor.forward(80, ROTATION)
right_motor.forward(80, ROTATION)