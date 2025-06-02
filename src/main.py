from machine import Pin, PWM
from servo import Servo
from ultrasonic import Ultrasonic
from encoded_motor import Motor
from time import sleep_ms
import os

class Logger:
    def __init__(self, filename) -> None:
        self.file = open(filename, 'a')
        self.file.write('-' * 20 + '\n')

    def log(self, message):
        self.file.write(f'{message}\n')
        self.file.flush()
        print(message)

    def close(self):
        self.file.close()

log_id = 1
for entry in os.ilistdir():
    if entry[1] == 0x8000:
        filename = entry[0]
        if filename.endswith('.log'):
            log_id += 1
logger = Logger(f'bot_{log_id}.log')

ROTATION = 22  # cm
## Your implementation goes here
# Servo = GPIO28
# Ultrasonic = { Echo: GPIO20, Trigger: GPIO21 }
# Left Motor = { Forward: 14, Reverse: 15, Speed: 13, Encoder : 3 }
# Right Motor = { Forward: 17, Reverse: 16, Speed: 18, Encoder : 4 }

left_motor = Motor(14, 15, 13, 3)
right_motor = Motor(17, 16, 18, 4)
sensor = Ultrasonic(20, 21)
servo = Servo(28)

def adjust_speed(speed):
    diff_distance = left_motor.distance_completed() - right_motor.distance_completed()
    logger.log(f'Checking speed adjustment: {diff_distance}')
    if diff_distance > 1:
        # right motor is going slower
        if right_motor.get_speed() < speed:
            # speed the right motor up if possible
            right_motor.change_speed(speed)
        else:
            # slow the left motor down
            left_motor.change_speed(left_motor.get_speed() - 1)
    elif diff_distance < -1:
        # left motor going slower
        if left_motor.get_speed() < speed:
            # speed the left motor up if possible
            left_motor.change_speed(speed)
        else:
            # slow the right motor down
            right_motor.change_speed(right_motor.get_speed() - 1)
  

# move the ultrasonic to face left, need to wait for the move to finish befor next action
servo.move(90)
sleep_ms(300)

# # move forward 22 cetimeters
left_motor.forward(80, 20)
right_motor.forward(80, 20)

# # wait for the move to be finished 
while left_motor.moving or right_motor.moving:
     sleep_ms(20)
     adjust_speed(80)

sleep_ms(300)
servo.move(90)
sleep_ms(1000)
distance = sensor.get_distance()
message = f'Forward distance is {distance}'
logger.log(message)


if distance <= (30):
    servo.move(90)
    distance = sensor.get_distance()
    message = f'Forward distance is {distance}'
    logger.log(message)
    left_motor.stop()
    right_motor.stop()
    left_motor.deinit()
    right_motor.deinit()
    sleep_ms(1000)
    servo.move(0)
    sleep_ms(1000)
    left_motor.forward(80, 18)
    right_motor.forward(0, 0)
    sleep_ms(1000)
    left_motor.stop()
    right_motor.stop()
    left_motor.deinit()
    right_motor.deinit()
    sleep_ms(1500)
    servo.move(90)
    sleep_ms(1000)
    distance = sensor.get_distance()
    message = f'Forward distance is {distance}'
    logger.log(message)
    if distance >= (15):
        left_motor.forward(80, 60)
        right_motor.forward(90, 60)
        while left_motor.moving or right_motor.moving:
            sleep_ms(20)
            adjust_speed(80)
        sleep_ms(1000)
        left_motor.forward(0, 0)
        right_motor.forward(80, 18)
        sleep_ms(1000)
        left_motor.stop()
        right_motor.stop()
        left_motor.deinit()
        right_motor.deinit()
