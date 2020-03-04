#!/usr/bin/env python

import serial
import time
from pprint import pprint
import sys
ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 57600#115200
#print(ser.read(200))
#sys.exit(0)
for x in range(30):
    #inst packet
    header = ser.read(4)
    print(header)
    send_id = ser.read(1)
    print(send_id)
    length_l = ser.read(1)
    length_h = ser.read(1)
    length =  int.from_bytes(length_l,byteorder='big') + (int.from_bytes(length_h,byteorder='big') << 8) - 3
    print(length)
    instruction = ser.read(1)
    print(instruction)
    params =':'.join(hex(i)[2:] for i in ser.read(length))
    chksum = ser.read(2)
    #full instruction packet!
    print('Instruction  Packet', 'Length:', length,
            'Instruction:', instruction,
            'Params:', params)
    #status Packet
    header = ser.read(4)
    send_id = ser.read(1)
    length_l = ser.read(1)
    length_h = ser.read(1)

    length =  max(int.from_bytes(length_l,byteorder='big') + (int.from_bytes(length_h,byteorder='big') << 8) - 4,0)
    instuction = ser.read(1)
    error = ser.read(1)
    params =':'.join(hex(i)[2:] for i in ser.read(length))
    chksum = ser.read(2)
    #full instruction packet!
    print('Status Packet', 'Length:', length,
            'Instruction:', instruction,
            'Error:', error,
            'Params:', params)


ser.close()

