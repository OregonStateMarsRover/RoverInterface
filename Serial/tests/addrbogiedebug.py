# Input information in the format:
# sudo python addrbogiedebug.py 1 3
# where 1 and 3 are addresses of wheels...
# This ordering will send speed packets addressed to 1 and then to 3
# NOTE: 1 does not exist, but that's okay... we are testing the checking
#       of addresses by the bogies

import sys
import time
sys.path.append('../')
import serial
from roverpacket import BogiePacket


def go(addr, speed, turning):
    packet = BogiePacket(addr, speed, turning)
    bus.write(packet.msg())
    print str(packet)

def grabAddrs():
    args = sys.argv
    if len(args) != 3:
        print "Needs addrs in format: sudo python addrbogiedebug.py 1 3"
    try:
        firstAddr = int(args[1])
        secondAddr = int(args[2])
    except:
        print "Needs addrs in format: sudo python addrbogiedebug.py 1 3"
    return firstAddr, secondAddr

if __name__ == '__main__':
    bus = serial.Serial(port='/dev/ttyUSB5',
                        baudrate=115200)
    speed_list = []
    firstAddr, secondAddr = grabAddrs()
    for x in range(1, 128):
        speed_list.append(x)
    for x in reversed(range(1, 127)):
        speed_list.append(x)
    for x in range(3):
        speed_list.append(0)
    for speed in speed_list:
        for wheelAddr in range(2, 8):
            go(bus, firstAddr, speed, 0)
            go(bus, secondAddr, speed, 0)
        time.sleep(0.04)
