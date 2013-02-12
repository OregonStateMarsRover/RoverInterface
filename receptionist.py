########## Receptionist ########## 

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO
# ordering. The Listener is launched in a separate thread to bring in messages
# from outside the GUI and Rover. Listener launches the Drive_Queuer and
# Arm_Queuer which use Rover_Status to find the values necessary to create
# tuples that the Listener can then use to have RoverPacket assemble packets.
# After this process is finished, the assembled packets are then added to the
# queue for the Receptionist to then execute.

import sys
sys.path.append('./Serial')
import serial
import time
import Queue
import threading
from roverpacket import *
from bus import *
from listener import *

# Receptionist
class Receptionist(object):
        def __init__(self):
                self.bus = Bus()
                self.queue = Queue.Queue()
                # This Listener listens to bus and adds messages to the queue
                self.listenerthread = Listener(self.bus, self.queue)
                self.listenerthread.start()
                self.start_time = time.clock()
                self.prev_time = 0
                self.count = 0

        # NOTE: When reading information from the queue, keep in mind that
        #       every item is a python list from 1-6 in length. But, the items
        #       in the python list are simply bytearrays that can be sent
        #       immediately.
        def start(self):
                count_start_time = time.clock() - self.start_time
                self.prev_time = time.clock()
                while 1:
                        if self.queue.empty() is False:
                                # NOTE: data is a python list that must be
                                #       iterated through
                                data = self.queue.get()
                                # Send at most 100 times per seconds
                                # If at least 20 milliseconds has passed, then
                                #       allow message to be passed
                                if (time.clock() - self.prev_time) > 0.02:
                                        self.prev_time = time.clock()
                                        # NOTE: ALLOW ALL 6 WHEEL PACKAGES TO
                                        #       BE SENT, BUT THEN THROW AWAY
                                        #       ALL THE OTHER MESSAGES BETWEEN.
                                        # CONSIDER 6 PACKET OF ALL WHEEL INFO
                                        #       AS 1 PACKAGE
                                        
                                        # Iterate through the python list and
                                        #       send each packet... this keeps
                                        #       certain packets together such
                                        #       as wheels 2-7
                                        for packet in data:
                                                self.count += 1
                                                print repr(packet)
                                                self.bus.rover.write(packet)
                                
                        if (time.clock() - count_start_time) > 1:
                        #        print "..................... This many \
                        #               messages/second: ", self.count
                                self.count = 0
                                count_start_time = time.clock() - self.start_time

if __name__ == '__main__':
        receptionist = Receptionist()
        receptionist.start()
