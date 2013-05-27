# tripodtest.py
# Mike Fortner
# Script for testing communication with the bogie controllers
# Use on the command line to generate packets over the serial port

import sys
import time
sys.path.append('../')
import serial
from roverpacket import TripodPacket

def exit_msg(sel=0):
    if sel == 0:
        print "Usage: {0} <address> <sub system> <command> <servo> <position high> <position low>".format(sys.argv[0].split("\\")[-1])
    elif sel == 1:
        print "Error: Values must be in range(0,256)"
    else:
        pass
    sys.exit(0)


def parse_input():
    args = sys.argv
    if len(args) != 7:
        exit_msg(0)
    try:
        addr = int(args[1])
	subsystem = int(args[2])
        command = int(args[3])
        servo = int(args[4])
        pos_high = int(args[5])
        pos_low = int(args[6])
    except ValueError as e:
        exit_msg(0)
    return (addr, subsystem, command, servo, pos_high, pos_low)

if __name__ == '__main__':
    addr, subsystem, command, servo, pos_high, pos_low = parse_input()
    print parse_input()
    try:
        packet = TripodPacket(addr, subsystem, command, servo, pos_high, pos_low)
    except ValueError as e:
        exit_msg(1)

    bus = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=38400)
    bus.write(packet.msg())
    print str(packet)
