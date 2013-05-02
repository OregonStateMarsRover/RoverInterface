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
<<<<<<< HEAD
    bus = serial.Serial(port='/dev/ttyUSB1',
=======
    bus = serial.Serial(port='/dev/ttyUSB0',
>>>>>>> f077da6114729811a438b3620ee4b29a6a2dc8e3
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
<<<<<<< HEAD
        #for wheelAddr in reversed(range(2, 4)):
        for addr in range(2,8):
		go(bus, addr, speed, 0)
        if (time.time() - start_time) > 1:
            # Send still alive message
            packet = BogiePacket(1, 17, 0)
            print str(packet)
            packet = packet.msg()
            bus.write(packet)
            start_time = time.time() # Reset timer
=======
        for wheelAddr in reversed(range(2, 8)):
        	go(bus, wheelAddr, speed, 0)
>>>>>>> f077da6114729811a438b3620ee4b29a6a2dc8e3
        time.sleep(burstSpeed)
