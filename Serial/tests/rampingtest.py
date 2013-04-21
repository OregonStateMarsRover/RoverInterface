import sys
import time
sys.path.append('../')
import serial
from roverpacket import BogiePacket


def go(bus, addr, speed, turning):
    packet = BogiePacket(addr, speed, turning)
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
    bus = serial.Serial(port='/dev/ttyUSB5',
                        baudrate=115200)
    start_time = time.time()
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
        #for wheelAddr in reversed(range(2, 4)):
        go(bus, 2, speed, 0)
        go(bus, 3, speed, 0)
        if (time.time() - start_time) > 1:
            # Send still alive message
            packet = BogiePacket(1, 17, 0)
            print str(packet)
            packet = packet.msg()
            bus.write(packet)
            start_time = time.time() # Reset timer
        time.sleep(0.1)