import Adafruit_DHT
import RPi.GPIO as GPIO

class Hardware():

    def __init__(self, sensorPin, ledPin):
        self._sensor = Adafruit_DHT.DHT11
        self._sensorPin = sensorPin
        self._ledPin = ledPin
        self._ledState = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ledPin, GPIO.OUT)
    
    def getSensorValues(self):
        return Adafruit_DHT.read_retry(self._sensor, self._sensorPin)

    def setLedState(self, state):
        self._ledState = state
        GPIO.output(self._ledPin, state)
        
    def getLedState(self):
        return self._ledState
