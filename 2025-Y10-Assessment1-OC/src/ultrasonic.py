from machine import Pin
import utime

class Ultrasonic:
    # Speed of sound in m/s
    SOUND_VELOCITY = 343
    def __init__(self, echo: int, trigger: int) -> None:
        # Initialise the ultrasonic sensor object with the specified Echo and Trigger pins
        self.echo = Pin(echo, Pin.IN)    # Set Echo pin as input
        self.trigger = Pin(trigger, Pin.OUT)    # Set Trigger pin as output

    def get_distance(self):
        """
        Measures the distance to an object using the ultrasonic sensor.

        The function works by sending a high pulse on the trigger pin, waiting 
        for the echo signal to be received, and then calculating the time it took
        for the sound wave to travel back. This is used to calculate the distance to
        the object. 

        Uses sleep but only 12us is used per request.

        Args:
            None

        Returns:
            float: The measured distance in centimetres.
        """
        self.trigger.low()
        utime.sleep_us(2)
        self.trigger.high()
        utime.sleep_us(10)
        self.trigger.low()

        while self.echo.value() == 0:
            signaloff = utime.ticks_us()
        
        while self.echo.value() == 1:
            signalon = utime.ticks_us()

        distance_time = utime.ticks_diff(signalon, signaloff) / 2
        # convert distance to centrimetres
        distance = round(Ultrasonic.SOUND_VELOCITY * distance_time / 10000, 2)
        return distance