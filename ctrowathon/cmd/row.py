#!/usr/bin/python
import struct
import serial
import time
import sys

def main():
    import random
    distance = 0
    while True:
        distance += random.random()
        print distance, 1
        sys.stdout.flush()
        time.sleep(0.10)


def main_real():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.open()
    while True:
        distance = get_distance(ser)
	t = get_time(ser)
        print distance, t
        sys.stdout.flush()
        time.sleep(0.10)

def get_distance(ser):
    ser.write("\xb0\x00")
    ser.flush()
    ser.read()
    return struct.unpack("f", ser.read(4))[0]

def get_time(ser):
    ser.write("\xb3\x00")
    ser.flush()
    ser.read()
    return struct.unpack("f", ser.read(4))[0]

if __name__ == '__main__':
    main()
