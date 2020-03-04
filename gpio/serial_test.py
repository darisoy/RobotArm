#!/usr/bin/env python

import serial
import time

ser = serial.Serial("/dev/ttyS0")
#ser.reset_input_buffer();
ser.baudrate = 57600 
#ser.write(b'\xff\xff\xfd\x00\x04\x03\x00\x01\x19\x0a')

ser.write(b'\x42')


#while True:
#    print(ser.read(8).hex())
ser.close()
