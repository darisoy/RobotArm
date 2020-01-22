import RPi.GPIO as GPIO
import sys
import time

if len(sys.argv) != 1:
    print('usage: <pin #>')
GPIO.setmode(GPIO.BOARD)

PIN = int(sys.argv[1], 10)
#VAL = int(sys.argv[2])

print(PIN)
GPIO.setup(PIN, GPIO.OUT)

while True:
    GPIO.output(PIN, 1)
    time.sleep(0.5)
    GPIO.output(PIN, 0)
    time.sleep(0.5)

