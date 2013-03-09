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
import time
from roverpacket import *
from bus import *
from queuer import *

class Receptionist(threading.Thread):
    def __init__(self, gui, roverStatus):
        threading.Thread.__init__(self)
        self.bus = Bus()
        self.gui = gui
        self.roverStatus = roverStatus
        # TODO: Add mutex around queuer
        self.queue = Queue.Queue()
        # Launch the queuer thread
        self.queuerthread = Queuer(gui, self.queue, roverStatus)
        self.queuerthread.start()

    # TODO: If the address is 2-7, then make a bogie packet
    # NOTE: Packets in queue are simply bytearrays that can be sent immediately
    def run(self):
        start_time = time.time()
        print "hello"
        while 1:
            if (time.time() - start_time) > 1:
                # Send still alive message
                packet = BogiePacket(1, 17, 0)
                packet = packet.msg()
                print self.queue.qsize
                self.queue.put(packet)
                print self.queue.qsize

                start_time = time.time() # Reset timer
            if self.queue.empty() is False:
                # Flush Output to keep it fresh
                packet = self.queue.get()
                print repr(packet)
                self.bus.rover.write(packet)
