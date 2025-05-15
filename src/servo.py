from machine import Pin, PWM

class Servo:
    __servo_pwm_freq = 50
    __min_u16_duty = 1640 - 2 # offset for correction
    __max_u16_duty = 7864 - 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001


    def __init__(self, pin):
        """ Create the servo object for controlling the servo motor """
        self.__initialise(pin)


    def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
        """
        Update the settings for the servo motor.

        Parameters:
            servo_pwm_freq (int): The PWM frequency for the servo motor.
            min_u16_duty (int): The minimum duty cycle value in 16-bit format.
            max_u16_duty (int): The maximum duty cycle value in 16-bit format.
            min_angle (float): The minimum angle of rotation in degrees.
            max_angle (float): The maximum angle of rotation in degrees.
            pin (int): The GPIO pin number connected to the servo motor.

        Returns:
            None
        """        
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u16_duty = min_u16_duty
        self.__max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, angle):
        """
        Moves the servo motor to the specified angle.

        Args:
            angle (float): The target angle in degrees to which the servo should be moved. The angle is rounded to 2 decimal places to reduce unwanted adjustments.

        Returns:
            None

        Raises:
            ValueError: If the provided angle is outside the valid range for the servo motor.
        """        
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        
        if angle < self.min_angle or angle > self.max_angle:
            raise ValueError(f"angle: '{angle}' is outside the angle range {self.min_angle}:{self.max_angle}")
        
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)

    def __angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty


    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)