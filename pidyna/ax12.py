'''
Based on Jesse Merritt's script:
https://github.com/jes1510/python_dynamixels
and Josue Alejandro Savage's Arduino library:
http://savageelectronics.blogspot.it/2011/01/arduino-y-dynamixel-ax-12.html
'''

from time import sleep
from serial import Serial
import RPi.GPIO as GPIO
import signal 

class Ax12_2:
    # important AX-12 constants
    # /////////////////////////////////////////////////////////// EEPROM AREA
    AX_MODEL_NUMBER_L = 0
    AX_MODEL_NUMBER_H = 1
    AX_VERSION = 2
    AX_ID = 3
    AX_BAUD_RATE = 4
    AX_RETURN_DELAY_TIME = 5
    AX_CW_ANGLE_LIMIT_L = 6
    AX_CW_ANGLE_LIMIT_H = 7
    AX_CCW_ANGLE_LIMIT_L = 8
    AX_CCW_ANGLE_LIMIT_H = 9
    AX_SYSTEM_DATA2 = 10
    AX_LIMIT_TEMPERATURE = 11
    AX_DOWN_LIMIT_VOLTAGE = 12
    AX_UP_LIMIT_VOLTAGE = 13
    AX_MAX_TORQUE_L = 14
    AX_MAX_TORQUE_H = 15
    AX_RETURN_LEVEL = 16
    AX_ALARM_LED = 17
    AX_ALARM_SHUTDOWN = 18
    AX_OPERATING_MODE = 19
    AX_DOWN_CALIBRATION_L = 20
    AX_DOWN_CALIBRATION_H = 21
    AX_UP_CALIBRATION_L = 22
    AX_UP_CALIBRATION_H = 23

    # ////////////////////////////////////////////////////////////// RAM AREA
    AX_TORQUE_STATUS = 24
    AX_LED_STATUS = 25
    AX_CW_COMPLIANCE_MARGIN = 26
    AX_CCW_COMPLIANCE_MARGIN = 27
    AX_CW_COMPLIANCE_SLOPE = 28
    AX_CCW_COMPLIANCE_SLOPE = 29
    AX_GOAL_POSITION_L = 30
    AX_GOAL_POSITION_H = 31
    AX_GOAL_SPEED_L = 32
    AX_GOAL_SPEED_H = 33
    AX_TORQUE_LIMIT_L = 34
    AX_TORQUE_LIMIT_H = 35
    AX_PRESENT_POSITION_L = 36
    AX_PRESENT_POSITION_H = 37
    AX_PRESENT_SPEED_L = 38
    AX_PRESENT_SPEED_H = 39
    AX_PRESENT_LOAD_L = 40
    AX_PRESENT_LOAD_H = 41
    AX_PRESENT_VOLTAGE = 42
    AX_PRESENT_TEMPERATURE = 43
    AX_REGISTERED_INSTRUCTION = 44
    AX_PAUSE_TIME = 45
    AX_MOVING = 46
    AX_LOCK = 47
    AX_PUNCH_L = 48
    AX_PUNCH_H = 49

    # /////////////////////////////////////////////////////////////// Status Return Levels
    AX_RETURN_NONE = 0
    AX_RETURN_READ = 1
    AX_RETURN_ALL = 2

    # /////////////////////////////////////////////////////////////// Instruction Set
    AX_PING = 1
    AX_READ_DATA = 2
    AX_WRITE_DATA = 3
    AX_REG_WRITE = 4
    AX_ACTION = 5
    AX_RESET = 6
    AX_SYNC_WRITE = 131

    # /////////////////////////////////////////////////////////////// Lengths
    AX_RESET_LENGTH = 2
    AX_ACTION_LENGTH = 2
    AX_ID_LENGTH = 4
    AX_LR_LENGTH = 4
    AX_SRL_LENGTH = 4
    AX_RDT_LENGTH = 4
    AX_LEDALARM_LENGTH = 4
    AX_SHUTDOWNALARM_LENGTH = 4
    AX_TL_LENGTH = 4
    AX_VL_LENGTH = 6
    AX_AL_LENGTH = 7
    AX_CM_LENGTH = 6
    AX_CS_LENGTH = 5
    AX_COMPLIANCE_LENGTH = 7
    AX_CCW_CW_LENGTH = 8
    AX_BD_LENGTH = 4
    AX_TEM_LENGTH = 4
    AX_MOVING_LENGTH = 4
    AX_RWS_LENGTH = 4
    AX_VOLT_LENGTH = 4
    AX_LOAD_LENGTH = 4
    AX_LED_LENGTH = 4
    AX_TORQUE_LENGTH = 4
    AX_POS_LENGTH = 4
    AX_GOAL_LENGTH = 5
    AX_MT_LENGTH = 5
    AX_PUNCH_LENGTH = 5
    AX_SPEED_LENGTH = 5
    AX_GOAL_SP_LENGTH = 7

    # /////////////////////////////////////////////////////////////// Specials
    AX_BYTE_READ = 1
    AX_INT_READ = 2
    AX_ACTION_CHECKSUM = 250
    AX_BROADCAST_ID = 254
    AX_START = 255
    AX_CCW_AL_L = 255
    AX_CCW_AL_H = 3
    AX_LOCK_VALUE = 1
    LEFT = 0
    RIGTH = 1
    RX_TIME_OUT = 10
    TX_DELAY_TIME = 0.002

    #//////////////////////////////////////////////////////////////// Protocol 2
    PREFIX = b'\xff\xff\xfd\x00'
    PING_LEN = b'\x03\x00'
    WRITE_LEN = b'\x09\x00'
    READ_LEN = b'\x07\x00'


    # RPi constants
    RPI_DIRECTION_PIN = 4
    RPI_DIRECTION_TX = GPIO.HIGH
    RPI_DIRECTION_RX = GPIO.LOW
    RPI_DIRECTION_SWITCH_DELAY = 0.0007

    # static variables
    port = None
    gpioSet = False

    def __init__(self):
        if(Ax12_2.port == None):
            Ax12_2.port = Serial("/dev/ttyS0", baudrate=57600, timeout=0.05)
            #print(Ax12_2.port)
        if(not Ax12_2.gpioSet):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Ax12_2.RPI_DIRECTION_PIN, GPIO.OUT)
            Ax12_2.gpioSet = True
        self.direction(Ax12_2.RPI_DIRECTION_RX)

    connectedServos = []

    # Error lookup dictionary for bit masking
    dictErrors = {  1 : "Input Voltage",
            2 : "Angle Limit",
            4 : "Overheating",
            8 : "Range",
            16 : "Checksum",
            32 : "Overload",
            64 : "Instruction"
            }

    # Custom error class to report AX servo errors
    class axError(Exception) : pass

    # Servo timeout
    class timeoutError(Exception) : pass

    def direction(self,d):
        GPIO.output(Ax12_2.RPI_DIRECTION_PIN, d)
        sleep(Ax12_2.RPI_DIRECTION_SWITCH_DELAY)

    def checksum(self,packet):
        crc_table = [
        0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
        0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
        0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
        0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
        0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
        0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
        0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
        0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
        0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
        0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
        0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
        0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
        0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
        0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
        0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
        0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
        0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
        0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
        0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
        0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
        0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
        0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
        0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
        0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
        0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
        0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
        0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
        0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
        0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
        0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
        0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
        0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
        ]
        accum = 0
        for j in packet:
            i = ((accum >> 8) ^ j) & 0xff
            accum = ((accum << 8) ^ crc_table[i])  & 0xffff
        return accum.to_bytes(2,byteorder='little')

    def readData(self,id):
        
        retval = None
        self.direction(Ax12_2.RPI_DIRECTION_RX)
        buf = b''
        num_errors = 0
        while buf[-4:] != Ax12_2.PREFIX:
            buf += self.port.read(1)
            #print(buf)
            if buf == b'':
                num_errors = num_errors+1
            if num_errors > 10:
                e = "Timeout on servo " + str(id)
                raise Ax12_2.timeoutError(e)

        reply = Ax12_2.port.read(5) # [0xff, 0xff,0xfd,0x00, origin, length_l,length_h,inst, error]
        reply = buf[-4:]+reply
        #print(reply.hex())
        #print(buf)
        try:
            assert reply[0] == 0xFF
        except:
            e = "Timeout on servo " + str(id)
            raise Ax12_2.timeoutError(e)

        try :
            length = reply[5]+(reply[6]<<8) - 4
            error = reply[8]

            if(error != 0):
                print ("Error from servo: " + Ax12_2.dictErrors[error] + ' (code  ' + hex(error) + ')') #TODO might be wrong
                retval = -error
            # just reading error byte

            if(length == 0):
                retval = bytes([error])
            else:
                retval = Ax12_2.port.read(length)
            #chksum = Ax12_2.port.read(2)
            #print(chksum)
            #print(retval)
        except axError as detail:
            raise Ax12_2.axError(detail)
        sleep(0.015)
        return retval

    def ping(self,id):
        self.direction(Ax12_2.RPI_DIRECTION_TX)
        Ax12_2.port.flushInput()
        outData = Ax12_2.PREFIX
        outData += bytes([id])
        outData += Ax12_2.PING_LEN
        outData += bytes([Ax12_2.AX_PING])
        #print(outData.hex())
        outData += self.checksum(outData)
        #print(outData.hex())
        Ax12_2.port.write(outData)
        while self.port.out_waiting: continue
        if (id != 6):
            sleep(0.0007)
        else:
            sleep(0.00052)
        return self.readData(id)

    def move(self, id, position):
        #print(position)
        new_position = int(position)
        if id == 6:
            new_position = int(new_position/4)
        self.direction(Ax12_2.RPI_DIRECTION_TX)
        Ax12_2.port.flushInput()
        p = [new_position&0xff, (new_position>>8)&0xff,0,0]
        #print(p)
        outData = Ax12_2.PREFIX
        outData += bytes([id])
        if id ==6:
            outData += b'\x07\x00'
        else:
            outData += Ax12_2.WRITE_LEN
        outData += bytes([Ax12_2.AX_WRITE_DATA])
        #0x0074 is the goal position register
        #print(outData.hex())
        if id ==6 :
            outData += b'\x1e\x00'
            outData += bytes(p[:2])
        else:
            outData += b'\x74\x00'
            outData += bytes(p)
        #print(outData.hex())

        outData += self.checksum(outData)
        
        #print(outData.hex())
        Ax12_2.port.write(outData)
        while self.port.out_waiting: continue
        if id != 6:
            sleep(0.0018)
        else:
            sleep(0.0014)
        #print('data sent')
        #try:
        #    return self.readData(id)
        #except axError as e:
            #return self.move(id,position)
        sleep(0.05)
        return None
    
    def moveDegrees(self, id, position):
        print(position)
        raw_pos = (position)*4096/360
        try:
            return self.move(id,raw_pos)
        except:
            return None
    
    def write(self, id, addr, val, length):
        self.direction(Ax12_2.RPI_DIRECTION_TX)
        Ax12_2.port.flushInput()
        outData = Ax12_2.PREFIX
        outData += bytes([id])
        outData += length #length write one param
        outData += bytes([Ax12_2.AX_WRITE_DATA])
        outData += addr
        outData += val 

        outData += self.checksum(outData)
        Ax12_2.port.write(outData)
        while self.port.out_waiting: continue
        sleep(0.0010)
        #print('data sent')
        return self.readData(id)

    def setTorqueStatus(self, id, status,verbose=False):
        self.direction(Ax12_2.RPI_DIRECTION_TX)
        Ax12_2.port.flushInput()
        outData = Ax12_2.PREFIX
        outData += bytes([id])
        outData += b'\x06\x00' #length write one param
        outData += bytes([Ax12_2.AX_WRITE_DATA])
        if id == 6:
            outData+=b'\x18\x00'
        else:
            outData += b'\x40\x00'
        #0x200 is 512 = 512/4096 = 45 degrees
        outData += b'\x01' if status else b'\x00'

        outData += self.checksum(outData)
        #print(outData.hex())
        if verbose: print('set torque: ', status, ' on servo #',id)
        Ax12_2.port.write(outData)
        while self.port.out_waiting: continue
        if (id != 6):
            sleep(0.0014)
        else:
            sleep(0.0011)
        #print('data sent')
        sleep(0.05)
        return None
        return self.readData(id)

    def readPosition(self, id):
        self.direction(Ax12_2.RPI_DIRECTION_TX)
        Ax12_2.port.flushInput()

        outData = Ax12_2.PREFIX
        outData += bytes([id])
        outData += Ax12_2.READ_LEN
        outData += bytes([Ax12_2.AX_READ_DATA])
        #0x0084 is the present position register
        outData += b'\x84\x00'
        outData += b'\x04\x00'

        outData += self.checksum(outData)
        #print(outData.hex())
        Ax12_2.port.write(outData)
        while self.port.out_waiting: continue
        sleep(0.0018)
        #print('data sent')
        
        position = self.readData(id)
        return position[0] + (position[1] << 8) + (position[2] <<16) + (position[3] << 24)
    
    def readPositionDegrees(self,id):
        raw = self.readPosition(id)
        return (raw*360/4096 +180) %360 -180

    def learnServos(self,minValue=1, maxValue=6, verbose=False) :
        servoList = []
        def timeout(signum, frame):
            raise IOError("Timeout")

        for i in range(minValue, maxValue + 1):
            try :
                signal.signal(signal.SIGALRM, timeout)
                signal.alarm(1)
                temp = self.ping(i)
                servoList.append(i)
                if verbose: print("Found servo #" + str(i))

            except Exception as detail:
                if verbose : print("Error pinging servo #" + str(i) + ': ' + str(detail))
                pass
        signal.alarm(0)
        return servoList

    def resetHome(self, id, ):
        self.direction(Ax12_2.RPI_DIRECTION_TX)
        Ax12_2.port.flushInput()
        outData = Ax12_2.PREFIX
        outData += bytes([id])
        outData += b'\x06\x00' #length write one param
        outData += bytes([Ax12_2.AX_WRITE_DATA])
        outData+=b'\x11\x11'#address
        outData += b'\x01' #value 
        outData += self.checksum(outData)
        Ax12_2.port.write(outData)
        while self.port.out_waiting: continue
        sleep(0.05)
        return None
