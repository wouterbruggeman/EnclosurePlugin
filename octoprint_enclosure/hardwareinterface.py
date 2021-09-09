import RPi.GPIO as GPIO
import os

import random

baseDir = '/sys/bus/w1/devices/'
dataFile = '/w1_slave'

class HardwareInterface:

    def __init__(self, plugin, led_pin, button_pin):
        self._plugin = plugin
        self._ledPin = led_pin

        self._ledState = False
        self._temperature = 0

        # GPIO settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        # Set led as output and set its state to false
        GPIO.setup(self._ledPin, GPIO.OUT)
        self.setLedState(False)
        
        # Add event to buttonpress
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=self._buttonPressed, bouncetime=200)

    def getLedState(self):
        return self._ledState

    def setLedState(self, state):
        self._ledState = state
        GPIO.output(self._ledPin, state)

    def _buttonPressed(self, pin):
        self.setLedState(~self.getLedState())

    def _readTemperatureFile(self):
        # Read the file
        f = open(baseDir + self._plugin._settings.get(['sensorName']) + dataFile)
        lines = f.readlines()
        f.close()
        return lines

    def getTemperature(self):
        if(not os.path.isfile(baseDir + self._plugin._settings.get(['sensorName']) + dataFile)):
            return "CONFIGURE SENSOR NAME 0"

        lines = self._readTemperatureFile()

        #Wait until the last 3 chars are equal to 'YES'
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._readTemperatureFile()
        
        #Find the index of t= in string
        tempPos = lines[1].find('t=')
        if tempPos != -1:
            return round(float(lines[1][tempPos+2:]) / 1000, 1)
