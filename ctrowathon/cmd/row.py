#!/usr/bin/python
import struct
import serial
import time
import sys

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.open()
    while True:
        distance = get_distance(ser)
        time.sleep(0.10)
        print distance
        sys.stdout.flush()

def get_distance(ser):
    ser.write("\xb0\x00")
    ser.flush()
    ser.read()
    return struct.unpack("f", ser.read(4))[0]

if __name__ == '__main__':
    main()
