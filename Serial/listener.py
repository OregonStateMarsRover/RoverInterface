########## Listener - listener.py ##########

# Original Author: John Zeller

# The Listener, listens to joy_queue for any incoming data tuples. When a data
# tuple comes the listener grabs it and uses RoverPacket to pack the data into
# a legitamite packet. It then adds this packet to the receptionists' queue

import sys
import serial
import time
import Queue
import threading
from roverpacket import *
from bus import *
from joy import *
from queuer import *

class Listener(threading.Thread):
    def __init__(self, bus, queue, roverStatus):
        threading.Thread.__init__(self)
        self.bus = bus
        self.queue = queue
        self.joy_queue = Queue.Queue()
        self.joythread = JoyParser(self.bus, roverStatus)
        self.joythread.start()
        self.queuerthread = Queuer(self.joy_queue, roverStatus)
        self.queuerthread.start()

# TODO: If the address is 2-7, then make a bogie packet
    def run(self):
		while 1:
				packet_list = []
				if self.joy_queue.empty() is False:
						packet_data = self.joy_queue.get()
						addr, speed, angle = packet_data
						packet = BogiePacket(addr, speed, angle)
						packet = packet.msg()	# Serializes packet
						packet_list.append(packet)
							
				self.queue.put(packet_list) # Add to recepetionists queue