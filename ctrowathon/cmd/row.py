#!/usr/bin/python
import sys
import time
import random

def main():
    val = 0
    while True:
        val += abs(random.gauss(0, 2))
        sys.stdout.write("%s\n" % val)
        sys.stdout.flush()
        time.sleep(0.10)

if __name__ == '__main__':
    main()
