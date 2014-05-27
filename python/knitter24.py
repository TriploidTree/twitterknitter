"""Communicates with TwitterKnitter hardware (i.e. Arduino)
over serial to send a pattern"""

import serial

class Knitter24:
    """Knitting machine (v1, 24 stitch patterns)"""
    
    def __init__(self, usb='/dev/ttyUSB0', baud=9600):
        self.serial = serial.Serial(usb, baud)

    def send_pattern(self, pattern):
        """Given a pattern as a list of 24-tuples, send it out over serial"""
        #write number of rows
        self.serial.write(chr(len(pattern)))

        for row in pattern:
            # we want to output LSB first
            byte3, byte2, byte1 = self.pack_row(row) 
            self.serial.write(chr(byte1))
            self.serial.write(chr(byte2))
            self.serial.write(chr(byte3))

    @classmethod
    def pack_row(cls, row):
        """Given a 24-value tuple, convert it to a tuple of three bytes"""
        #assumption: tuple was 24 items long and contained only '0' and '1'
        binary_pattern = [str(x) for x in row]
        row_string = ''.join(binary_pattern)
        return (int(row_string[0:8], 2), 
                int(row_string[8:16], 2), 
                int(row_string[16:24], 2))