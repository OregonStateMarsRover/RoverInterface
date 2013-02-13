########## Receptionist - receptionist.py ########## 

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO
# ordering. The Listener is launched in a separate thread to bring in messages
# from outside the GUI and Rover. Listener launches the Drive_Queuer and
# Arm_Queuer which use Rover_Status to find the values necessary to create
# tuples that the Listener can then use to have RoverPacket assemble packets.
# After this process is finished, the assembled packets are then added to the
# queue for the Receptionist to then execute.

# TO DO
# Make GUI that shows what receptionist is currently sending from its queue
# Perhaps organize these into the

# TO DO 2
# Make GUI launch bus and handle which controller is which port

import sys
sys.path.append('./Serial')
import serial
import time
import Queue
import threading
from roverpacket import *
from bus import *
from listener import *

class Receptionist(object):
    def __init__(self, roverStatus):
        self.bus = Bus()
        self.queue = Queue.Queue()
        # This Listener listens to bus and adds messages to the queue
        self.listenerthread = Listener(self.bus, self.queue,
                                       roverStatus)
        self.listenerthread.start()

    # NOTE: Packets in queue are simply bytearrays that can be sent immediately
    def start(self):
        while 1:
            if self.queue.empty() is False:
                # NOTE: 'data' is a python list that must be iterated through
                data = self.queue.get()
                for packet in data:
                    print repr(packet)
 #OFF ROVER TEST                    self.bus.rover.write(packet)