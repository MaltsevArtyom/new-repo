import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
state = 0
period = 5.0

while True:
    state = not state
    GPIO.output(led, state)
    time.sleep(period)


