########## Listener ##########

# Original Author: John Zeller

# The Listener, listens to rover bus line for any incoming packets and to the
# joys for any incoming telemetry. When a packet comes the listener grabs it
# and stores it into the queue for the receptionist

# Needing to implement
# 	Read 1 list at a time from the joy_queue. This list is going to have
#	between 3 and 6 lists for 3-6 wheels. Listener needs to create a set of 6
#	packets from these and then add them to the receptionists queue all at the
#	same time to ensure that they are all executed next to one another. ie no
#	other packet is put amongst a set of 3-6 wheel packets

# Ideas
# 	Maybe create a second Listener JUST for joy

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

#### old code that runs
#		temp_list = []
#		
#                while 1:
#                        if self.joy_queue.empty() is False:
#				data = self.joy_queue.get()
#				# Iterate through each wheel in this packet
#				for wheel in data:
#					# Break data into individual variables
#					addr, speed, angle = wheel	# Tuple
#					# Translate data into packets ready to send to receptionist
#					packet = BogiePacket(addr, speed, angle)
#					# Send packet to receptionist's queue
#					self.queue.put(packet.msg())		
                
                while 1:
			packet_list = []
                        if self.joy_queue.empty() is False:
				data = self.joy_queue.get()
				# Iterate through each wheel in this packet
				for wheel in data:
					# Break data into individual variables
					addr, speed, angle = wheel	# Tuple
					# Translate data into packets ready to send to receptionist
					packet = BogiePacket(addr, speed, angle)
					# Send packet to receptionist's queue
					packet = packet.msg()	# packet.msg() serializes packet
					packet_list.append(packet)
				self.queue.put(packet_list)
			#if self.some_other_queue.empty() is False:
				# Do some other thing
				
				