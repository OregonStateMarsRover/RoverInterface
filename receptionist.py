########## Receptionist ########## 

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO ordering.
# The Listener is launched in a separate thread to bring in messages from outside the
# BeagleBone and adds them to the queue for the Receptionist to then execute.

# Ideas
# 	Maybe create a second Listener JUST for joy

import sys
sys.path.append('/home/rover/RoverInterface/Serial')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *
from listener import *

# Initialization of interrupts



# Receptionist
class Receptionist(object):
        def __init__(self):
                # Create bus object which holds all initialized ports
                self.bus = Bus()
                # Create queue object which holds all packets waiting to be used
                self.queue = Queue.Queue()
                # Create listener object which will be launched on another thread
                # This listener, listens to every port and adds messages to the queue
                self.listenerthread = Listener(self.bus, self.queue)
                self.listenerthread.start()
                self.start_time = time.clock()
                self.prev_time = 0

        def start(self):
                while 1:
                        if self.queue.empty() is False:
                                data = self.queue.get()
                                self.bus.rover.write(data)
                                


if __name__ == '__main__':
        receptionist = Receptionist()
        receptionist.start()
