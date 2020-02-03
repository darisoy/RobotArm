#!/usr/bin/env python
from ax12 import Ax12_2
import time
def main():
    servo_bus = Ax12_2()
    #packet = '\xff\xff\xfd\x00\x01\x03\x00\x01'
    #print(hex(servo_bus.checksum(packet)))
    print("----ping start----")
    print(servo_bus.ping(4).hex())
    #print(servo_bus.ping(5).hex())
    #print("----torque enable-")
    print(servo_bus.setTorqueStatus(4,True))
    #print(servo_bus.setTorqueStatus(5,True))
    #print("----move start----")
    #print(servo_bus.move(4, 116).hex())
    #print(servo_bus.move(5, 116).hex())
    while True:
        servo_bus.move(4,3500)
        #servo_bus.move(5,0)
        time.sleep(2)
        servo_bus.move(4,0)
        #servo_bus.move(5,2048)
        #servo_bus.ping(1)
        time.sleep(2)
#    servo_bus.ping(1)
#    while True:
#        servo_bus.setLedStatus(1,True)
#        time.sleep(1)
#        servo_bus.setLedStatus(1,False)
#        time.sleep(0.5)
if __name__ == '__main__':
    main()
