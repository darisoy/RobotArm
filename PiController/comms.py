from time import sleep
from serial import Serial
import RPi.GPIO as GPIO
import signal

class Messages:
    #Instruction Set
    INSTR_PING = 1
    INSTR_READ_DATA = 2
    INSTR_WRITE_DATA = 3
    INSTR_REG_WRITE = 4
    INSTR_ACTION = 5
    INSTR_RESET = 6

    #Protocol 2
    PREFIX =    b'\xff\xff\xfd\x00'
    PING_LEN =  b'\x03\x00'
    WRITE_LEN = b'\x09\x00'
    READ_LEN =  b'\x07\x00'

    # RPi constants
    DIRECTION_PIN = 4
    DIRECTION_TRANSMIT = GPIO.HIGH
    DIRECTION_RECIEVE = GPIO.LOW
    DIRECTION_SWITCH_DELAY = 0.0007

    def __init__(self):
        self.port = Serial("/dev/ttyS0", baudrate=1000000, timeout=0.05)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIRECTION_PIN, GPIO.OUT)
        self.__direction(self.DIRECTION_RECIEVE)

    def moveDegrees(self, id, position):
        print(id,'->',position)
        raw_pos = position * 4096 / 360
        return self.__sendMoveMessage(id, raw_pos)

    def __sendMoveMessage(self, id, raw_position):
        self.__direction(self.DIRECTION_TRANSMIT)
        self.port.flushInput()
        processed_position = self.__processRawPosition(raw_position)
        comms_message = self.__constructMoveMessage(id, processed_position)
        self.port.write(comms_message)
        while self.port.out_waiting:
            continue
        self.__delayAfterMoveMessage(id)
        self.__direction(self.DIRECTION_RECIEVE)
        sleep(0.07)

    def __processRawPosition(self, raw_position):
        int_position = int(raw_position)
        processed_position = [int_position & 0xff, (int_position >> 8) & 0xff, 0, 0]
        return processed_position

    def __constructMoveMessage(self, id, position):
        comms_message = self.PREFIX
        comms_message += bytes([id])
        if id >=6:
            comms_message += b'\x07\x00'
            comms_message += bytes([self.INSTR_WRITE_DATA])
            comms_message += b'\x1e\x00'
            comms_message += bytes(position[:2])
        else:
            comms_message += self.WRITE_LEN
            comms_message += bytes([self.INSTR_WRITE_DATA])
            comms_message += b'\x74\x00'
            comms_message += bytes(position) #goal position register
        comms_message += self.__checksum(comms_message)
        return comms_message

    def __delayAfterMoveMessage(self, id):
        if id < 6:
            sleep(0.0018)
        else:
            sleep(0.0014)

    def enableTorque(self, id):
        self.__direction(self.DIRECTION_TRANSMIT)
        self.port.flushInput()
        comms_message = self.__constructEnableTorqueMessage(id)
        self.port.write(comms_message)
        print('enabled torque on joint #',id)
        while self.port.out_waiting:
            continue
        self.__direction(self.DIRECTION_RECIEVE)

    def __constructEnableTorqueMessage(self, id):
        comms_message = self.PREFIX
        comms_message += bytes([id])
        comms_message += b'\x06\x00' #length write one param
        comms_message += bytes([self.INSTR_WRITE_DATA])
        if id >= 6:
            comms_message+=b'\x18\x00'
        else:
            comms_message += b'\x40\x00'
        comms_message += b'\x01'
        comms_message += self.__checksum(comms_message)
        return comms_message

    def __delayAfterEnableTorque(self, id):
        if (id < 6):
            sleep(0.0014)
        else:
            sleep(0.0011)
        sleep(0.05)

    def __direction(self,d):
        GPIO.output(self.DIRECTION_PIN, d)
        sleep(self.DIRECTION_SWITCH_DELAY)

    def __checksum(self,packet):
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
            accum = ((accum << 8) ^ crc_table[i]) & 0xffff
        return accum.to_bytes(2, byteorder='little')
