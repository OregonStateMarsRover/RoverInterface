########## Receptionist - receptionist.py ##########

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
        self.roverStatus = roverStatus
        self.queue = Queue.Queue()
        self.queuerthread = Queuer(gui, self.queue, roverStatus)
        self.queuerthread.start()

    # TODO: If the address is 2-7, then make a bogie packet
    # NOTE: Packets in queue are simply bytearrays that can be sent immediately
    def run(self):
        start_time = time.time()
        while 1:
            # Send still alive message every 1 second
            if (time.time() - start_time) > 1:
                packet = BogiePacket(1, 17, 0)
                packet = packet.msg()
                with self.roverStatus.queueMutex:
                    self.queue.put(packet)
                start_time = time.time() # Reset timer
            if self.queue.empty() is False:
                # Flush Output to keep it fresh
                with self.roverStatus.queueMutex:
                    packet = self.queue.get()
                print repr(packet)
                try:
                    self.bus.rover.write(packet)
                except:
                    #print 'bus.rover not working'
                    try:
                        self.bus.restart('rover')
                    except:
                        #print "bus.rover still cannot start"
                        continue
                    continue