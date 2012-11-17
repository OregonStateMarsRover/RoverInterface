########## Listener ##########

# Original Author: John Zeller

# The Listener, listens to rover bus line for any incoming packets and to the joys
# for any incoming telemetry. When a packet comes the listener grabs it and stores
# it into the queue for the receptionist

import sys
sys.path.append('/home/rover/RoverInterface/Serial')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *
from joy import *

class Listener(threading.Thread):
        def __init__(self, bus, queue):
                # Initializes threading
                threading.Thread.__init__(self)
                # Stores the bus and queue objects
                self.bus = bus
                self.queue = queue
		self.joy_queue = Queue.Queue()
		self.joythread = JoyParser(self.bus, self.joy_queue)
                self.joythread.start()

        def run(self):
		# If the address is 2-7, then make a bogie packet
		
                list = []
                while 1:
                        if self.bus.base.inWaiting() > 0:
                                list.append(self.bus.base.read(1))
                        elif (self.bus.base.inWaiting() == 0) and (list != []):
                                self.queue.put(list)
                                list = []
