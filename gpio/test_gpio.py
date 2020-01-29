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

for i in range(30):
    GPIO.output(PIN, 1)
    time.sleep(0.6)
    GPIO.output(PIN, 0)
    time.sleep(0.6)
GPIO.cleanup()
