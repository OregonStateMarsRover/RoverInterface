import sys
import time
sys.path.append('../')
import serial
from roverpacket import BogiePacket


def go(addr, speed, turning):
    packet = BogiePacket(addr, speed, turning)

    bus = serial.Serial(port='/dev/ttyUSB1',
                        baudrate=115200)
    bus.write(packet.msg())
    print str(packet)


def grabBurstSpeed():
    args = sys.argv
    if len(args) != 2:
        print "Needs speed in format: python rampingtest.py 20 where 20 is in ms"
    try:
        burstSpeed = float(args[1])
    except:
        print "Needs speed in format: python rampingtest.py 20 where 20 is in ms"
    return burstSpeed

if __name__ == '__main__':
    burstSpeed = float(grabBurstSpeed()) / 1000
    speed_list = []
    count = 0
    for x in range(1, 128):
        speed_list.append(x)
    for x in reversed(range(1, 127)):
        speed_list.append(x)
    for x in range(3):
	speed_list.append(0)
    for speed in speed_list:
        for wheelAddr in range(2, 8):
            go(wheelAddr, speed, 0)
        time.sleep(0.04)

        time.sleep(burstSpeed)
