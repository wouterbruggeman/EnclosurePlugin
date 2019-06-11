import Adafruit_DHT
import RPi.GPIO as GPIO

class Hardware():

    def __init__(self, sensorPin, ledPin, buttonPin):
        self._sensor = Adafruit_DHT.DHT11
        self._sensorPin = sensorPin
        self._ledPin = ledPin
        self._buttonPin = buttonPin
        self._ledState = False

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ledPin, GPIO.OUT)
        GPIO.setup(self._buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._buttonPin, GPIO.FALLING, callback=self.buttonPressed, bouncetime=200)

        GPIO.output(self._ledPin, False)
    
    def getSensorValues(self):
        return Adafruit_DHT.read_retry(self._sensor, self._sensorPin)

    def setLedState(self, state):
        self._ledState = state
        GPIO.output(self._ledPin, state)
        
    def getLedState(self):
        return self._ledState

    def buttonPressed(self, pin):
        self.setLedState(~self._ledState);
