#!/usr/bin/env python
from ax12 import Ax12_2
import time
def main():
    servo_bus = Ax12_2()
    #packet = '\xff\xff\xfd\x00\x01\x03\x00\x01'
    #print(hex(servo_bus.checksum(packet)))
    servo_bus.ping(4)
#    servo_bus.ping(1)
#    while True:
#        servo_bus.setLedStatus(1,True)
#        time.sleep(1)
#        servo_bus.setLedStatus(1,False)
#        time.sleep(0.5)
if __name__ == '__main__':
    main()
