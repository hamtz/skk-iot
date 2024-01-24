import wiringpi
import time
from wiringpi import GPIO
wiringpi.wiringPiSetup()

wiringpi.pinMode(2,GPIO.OUTPUT)

wiringpi.digitalWrite(2,GPIO.HIGH)
time.sleep(5)
wiringpi.digitalWrite(2,GPIO.LOW)
