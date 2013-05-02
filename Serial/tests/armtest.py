########## Arm Test - armtest.py ##########

# Original Author: Mike Fortner and John Zeller
# Script for testing communication with the arm controller
# Use on the command line to generate packets over the serial port

# Keep in mind these addresses:
# 8 - Arm   (secondAddr, angle, angle_overflow)
#   + 1 - Shoulder Motor
#   + 2 - Elbow Motor

import sys
sys.path.append('../')
import serial
from roverpacket import ArmPacketLong


def exit_msg(sel=0):
    if sel == 0:
        print "Usage: {0} <address> <secAddr> <angle> - where angle is 0-360".format(sys.argv[0].split("\\")[-1])
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
        secAddr = int(args[2])
        angle = int(args[3])
    except ValueError as e:
        exit_msg(0)
    angle_overflow = 0
    if angle > 180:
        angle_overflow = angle - 180
        angle = 180
    return (addr, secAddr, angle, angle_overflow)

if __name__ == '__main__':
    addr, secAddr, angle, angle_overflow = parse_input()
    print parse_input()
    try:
        packet = ArmPacketLong(addr, secAddr, angle, angle_overflow)
    except ValueError as e:
        exit_msg(1)

    bus = serial.Serial(port='/dev/ttyUSB0',
                        baudrate=115200)
    bus.write(packet.msg())
    print str(packet)
