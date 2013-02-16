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
import Queue
import threading
from roverpacket import *
from bus import *
from queuer import *


class Receptionist(threading.Thread):
    def __init__(self, roverStatus):
        threading.Thread.__init__(self)
        self.bus = Bus()
        # TODO: Add mutex around queuer
        self.queue = Queue.Queue()
        # Launch the queuer thread
        self.queuerthread = Queuer(self.queue, roverStatus)
        self.queuerthread.start()

    # TODO: If the address is 2-7, then make a bogie packet
    # NOTE: Packets in queue are simply bytearrays that can be sent immediately
    def run(self):
        while 1:
            if self.queue.empty() is False:
                #print "InWaiting(): " + str(self.bus.rover.inWaiting())
                # Flush Output to keep it fresh
                #self.bus.rover.flushOutput()
                packet = self.queue.get()
                print repr(packet)

 # OFF ROVER TEST                    self.bus.rover.write(packet)
