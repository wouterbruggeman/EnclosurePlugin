import Adafruit_DHT

class Hardware():

    def __init__(self, sensorPin):
        self._sensor = Adafruit_DHT.DHT11
        self._sensorPin = sensorPin
    
    def getSensorValues(self):
        return Adafruit_DHT.read_retry(self._sensor, self._sensorPin)
