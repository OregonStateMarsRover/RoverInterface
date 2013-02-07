########## Listener ##########

# Original Author: John Zeller

# The Listener, listens to rover bus line for any incoming packets and to the joys
# for any incoming telemetry. When a packet comes the listener grabs it and stores
# it into the queue for the receptionist

# Needing to implement
# 	Read 1 list at a time from the joy_queue. This list is going to have between
# 	3 and 6 lists for 3-6 wheels. Listener needs to create a set of 6 packets
# 	from these and then add them to the receptionists queue all at the same time
# 	to ensure that they are all executed next to one another. ie no other packet
# 	is put amongst a set of 3-6 wheel packets

# Ideas
# 	Maybe create a second Listener JUST for joy

import sys
sys.path.append('/home/rover/RoverInterface/Serial')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *
from joy_main import *

class Listener(threading.Thread):
        def __init__(self, bus, queue):
                # Initializes threading
                threading.Thread.__init__(self)
                # Stores the bus and queue objects
                self.bus = bus
                self.queue = queue
		self.joy_queue = Queue.Queue()
		self.joythread = JoyPoller(self.bus, self.joy_queue)
                self.joythread.start()

        def run(self):
		# If the address is 2-7, then make a bogie packet
		
                list = []
                #while 1:
                #        if self.bus.base.inWaiting() > 0:
                #                list.append(self.bus.base.read(1))
                #        elif (self.bus.base.inWaiting() == 0) and (list != []):
                #                self.queue.put(list)
                #                list = []
                while 1:
			# Check to see if joy has a packet ready - 0 is an escape byte
                        if self.joy_queue.empty() is False:
				# Grab data
				data = self.joy_queue.get()
				#self.queue.put(data)
				# Iterate through each wheel in this packet
				for wheel in data:
					# Break data into individual variables
					addr, speed, angle = wheel	# Tuple
					if speed < 0:
						speed = -(speed) 	# WARNING THIS CAUSES ONLY FORWARD VALUES
					# Translate data into packets ready to be sent to receptionist
					packet = BogiePacket(addr, speed, angle)
					# Send packet to receptionist's queue
					print packet
					self.queue.put(packet.msg())	# packet.msg() serializes the packet
			#if self.some_other_queue.empty() is False:
				# Do some other thing
				
				