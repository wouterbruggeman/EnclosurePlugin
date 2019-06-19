import Adafruit_DHT
import RPi.GPIO as GPIO

import threading

class HardwareThread(threading.Thread):

    def __init__(self, plugin, sensorPin, ledPin, buttonPin, sensorUpdateInterval):
        threading.Thread.__init__(self)

        self._sensorUpdateInterval = sensorUpdateInterval
        self._plugin = plugin
        self._running = True
        
        #Pins etc
        self._sensor = Adafruit_DHT.DHT11
        self._sensorPin = sensorPin
        self._ledPin = ledPin
        self._buttonPin = buttonPin
        
        #Values for the leds and sensor
        self._ledState = False
        self._sensorValues = [0,0]
        
        #GPIO settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        #Set led as output and set its state to false
        GPIO.setup(self._ledPin, GPIO.OUT)
        GPIO.output(self._ledPin, False)
        
        #Add event to buttonpress
        GPIO.setup(self._buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._buttonPin, GPIO.FALLING, callback=self._buttonPressed, bouncetime=200)

    def run(self):
        while(self._running):
            self._updateSensorValues()

    def stop(self):
        self._running = False

    def _buttonPressed(self, pin):
        self.setLedState(~self._ledState);
        
    def _updateSensorValues(self):
        newValues = Adafruit_DHT.read_retry(self._sensor, self._sensorPin)
        if(newValues != (None, None)):
            self._sensorValues = newValues

        self._plugin._logger.info(newValues)
        self._plugin._logger.info("Updated sensor values!")

    def getSensorValues(self):
        return self._sensorValues

    def setLedState(self, state):
        self._ledState = state
        GPIO.output(self._ledPin, state)
        
    def getLedState(self):
        return self._ledState
