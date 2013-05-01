# bogietest.py
# Mike Fortner
# Script for testing communication with the bogie controllers
# Use on the command line to generate packets over the serial port

import sys
sys.path.append('../')
import serial
from roverpacket import BogiePacket


def exit_msg(sel=0):
    if sel == 0:
        print "Usage: {0} <address> <speed> <turn angle>".format(sys.argv[0].split("\\")[-1])
    elif sel == 1:
        print "Error: Values must be in range(0,256)"
    else:
        pass
    sys.exit(0)


def parse_input():
    args = sys.argv
    if len(args) != 4:
        exit_msg(0)
    try:
        addr = int(args[1])
        speed = int(args[2])
        turning = int(args[3])
    except ValueError as e:
        exit_msg(0)
    return (addr, speed, turning)

if __name__ == '__main__':
    addr, speed, turning = parse_input()
    print parse_input()
    try:
        packet = BogiePacket(addr, speed, turning)
        packet2 = BogiePacket(addr, turning, speed)
    except ValueError as e:
        exit_msg(1)

    bus = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=115200)
    bus.write(packet.msg())
    print str(packet)
