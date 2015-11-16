import serial
import struct

BAUD_RATE = 115200

class KeyCommException(EnvironmentError):
    pass

class KeyDevice:
    
    def __init__(self, port_name):
        self.com = serial.Serial(port_name, BAUD_RATE, timeout=20)

    def get_id(self):
        print(1)
        self.com.write(("1  ").encode())
        print(2)
        self.com.flush()
        print(3)
        line = self.com.readline()
        packet_type = int(line)
        print(line)
        if packet_type == 2:
            uuid = int(self.com.readline())
            return uuid
        else:
            raise KeyCommException()

    def encrypt(self, nonce):
        self.com.write(str(3) + "\n")
        self.com.write(str(nonce) + "\n")
        packet_type = int(self.com.readline())
        if packet_type == 2:
            echoed_nonce = int(self.com.readline())
            encrypted_nonce = int(self.com.readline())
            if echoed_nonce != nonce:
                KeyCommException()
            return encrypted_nonce
        else:
            raise KeyCommException()
        

def numToBytes(num, numBytes):
    b = bytearray(numBytes)
    for i in xrange(numBytes):
        quotient = num / 256
        remainder = num % 256;
        b[numBytes - i - 1] = remainder
        num = quotient
    return b

def bytesToNum(b):
    num = 0
    for digit in b:
        num += digit
        num *= 256
    return num / 256
