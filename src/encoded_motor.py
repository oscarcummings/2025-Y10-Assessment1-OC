from machine import Pin, PWM

class Motor:
    PWM_FREQ = 1000
    PWM_DUTY = 512
    MAX_DUTY = 65536
    ENCODER_SLOTS = 20
    WHEEL_CIRC = 22  # centimeters
    # PWM_FREQ = 15000
    # PWM_DUTY = 750
    # MAX_DUTY = 1023

    def __init__(self, forward, reverse, speed, encoder) -> None:
        self.forward_pin = Pin(forward, Pin.OUT)
        self.reverse_pin = Pin(reverse, Pin.OUT)
        self.encoder_pin = Pin(encoder, Pin.IN)
        self.pwm = PWM(Pin(speed))
        self.pwm.freq(Motor.PWM_FREQ)
        self.pwm.duty_u16(Motor.PWM_FREQ)
        self.encoder_pin.irq(handler=self.distance_travelled, trigger=Pin.IRQ_FALLING)
        self.distance_counter = 0
        self.distance = 0    # centimetres
        self.moving = False
        self.speed = 0

    def get_speed(self):
        return self.speed
    
    def change_speed(self, speed):
        self.speed = speed
        self.pwm.duty_u16(self._speed_actual(speed))

    def distance_completed(self):
        return self.distance_counter * (Motor.WHEEL_CIRC / Motor.ENCODER_SLOTS)

    def distance_travelled(self, pin):
        self.distance_counter += 1
        
        if self.distance_counter * (Motor.WHEEL_CIRC / Motor.ENCODER_SLOTS) >= self.distance:
            self.stop()
            print(self.distance_counter)
            self.moving = False
            self.distance = 0
            self.distance_counter = 0

    def forward(self, speed, distance):
        if self.moving:
            print('Still moving, next command ignored')
            return False
        self.moving = True
        self.distance_counter = 0            
        self.distance = distance
        self.forward_pin.high()
        self.reverse_pin.low()
        self.pwm.duty_u16(self._speed_actual(speed))
        return True

    def reverse(self, speed, distance):
        if self.moving:
            print('Still moving, next command ignored')
            return False
        self.moving = True
        self.distance = distance
        self.forward_pin.low()
        self.reverse_pin.high()
        self.pwm.duty_u16(self._speed_actual(speed))
        return True

    def stop(self):
        self.forward_pin.low()
        self.reverse_pin.low()
        self.moving = False
        self.pwm.duty_u16(0)

    def is_moving(self):
        return self.moving
    
    def _speed_actual(self, speed):
        return int(speed / 100 * Motor.MAX_DUTY)

    def deinit(self):
        self.pwm.deinit()