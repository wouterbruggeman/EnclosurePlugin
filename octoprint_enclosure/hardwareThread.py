import RPi.GPIO as GPIO
import threading, time, os

baseDir = '/sys/bus/w1/devices/'
dataFile = '/w1_slave'

class HardwareThread(threading.Thread):

    def __init__(self, plugin, sensorPin, ledPin, buttonPin):
	threading.Thread.__init__(self)
        self._plugin = plugin
        self._running = True
        
        #Pins etc
        self._sensorPin = sensorPin
        self._ledPin = ledPin
        self._buttonPin = buttonPin
        
        #Values for the leds and sensor
        self._ledState = False
        self._temperature = 0
        
        #GPIO settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        #Set led as output and set its state to false
        GPIO.setup(self._ledPin, GPIO.OUT)
        GPIO.output(self._ledPin, False)
        
        #Add event to buttonpress
        GPIO.setup(self._buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._buttonPin, GPIO.FALLING, callback=self._buttonPressed, bouncetime=200)
    
    def stop(self):
        self._running = False

    def run(self):
        while(self._running):
            self._updateSensorValues()
            self._plugin._logger.info(self.getTemperature())
            #time.sleep(float(self._plugin._settings.get(['sensorUpdateInterval'])))
            time.sleep(5)
    
    def _readTemperatureFile(self):
        #Read the file
        f = open(baseDir + '28-0116258ec9ee' + dataFile)
        lines = f.readlines()
        f.close()
        return lines

    def _updateSensorValues(self):
        lines = self._readTemperatureFile()

        #Wait until the last 3 chars are equal to 'YES'
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._readTemperatureFile()
        
        #Find the index of t= in string
        tempPos = lines[1].find('t=')
        if tempPos != -1:
            self._temperature = float(lines[1][tempPos+2:]) / 1000

    def _buttonPressed(self, pin):
        self.setLedState(~self._ledState);
        
    def getTemperature(self):
        return self._temperature

    def setLedState(self, state):
        self._ledState = state
        GPIO.output(self._ledPin, state)
        
    def getLedState(self):
        return self._ledState
