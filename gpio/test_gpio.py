import RPi.GPIO as GPIO
import sys
import time

if len(sys.argv) != 1:
    print('usage: <pin #>')
GPIO.setmode(GPIO.BOARD)

PIN = 33
#int(sys.argv[1], 10)
#VAL = int(sys.argv[2])

print(PIN)
GPIO.setup(PIN, GPIO.IN)

try:
        while True:
            if GPIO.input(PIN):
                print ("HOME PRESSED")
            time.sleep(0.1)
finally:
    GPIO.cleanup()
