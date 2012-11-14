############ XBox Controller Parser - joy.py ##########

# Original Author: John Zeller

# Joy parses data coming from the Xbox controller and adds it to joy_queue
# Listener is listening to what Joy places into this queue and will package
# and send the appropriate information to the receptionist

### Abilities ###########################################################
# LJ - Controls all left wheels forward/reverse (no left/right) 	#
# RJ - Controls all right wheels forward/reverse (no left/right)	#
# LT - Throttles a 0-point skid steer to the left			#
# RT - Throttles a 0-point skid steer to the right			#
# LB - Rotates actuator motors clockwise (when looking from top)	#
# RB - Rotates actuator motors counterclockwise (when looking from top) #
#########################################################################

### Soon-to-come Abilities ##############################################
# D-Pad - Tripod Controls						#
# Middle - Emergency Stop All Systems					#
# Y - Actuate motor to create 0-point turn form				#
#########################################################################

### NOTES #######################################################
# 1) LEAVE MODE 'OFF' there is no support in joy.py for MODE ON #
# 2) This parser was built using this tutorial as a reference:	#
#	http://hackshark.com/?p=147#axzz2BHTVXCFz		#
#################################################################

#### Buttons/Joys Represented: ##################################
# A, B, X, Y, RB, LB, LJButton, RJButton, Back, Start, Middle	#
# RT, LT, LeftJoy, RightJoy					#
#################################################################

#### Possible Additions: ################################################################
# 1) When the Joy hits back to 0, then send a 0 speed command... sometimes it ends with	#
#    a speed value other than 0								#
# 2) In case of artifacts in serial communication, initialize communication with all 0	#
#    values for speeds, just in case the rover is given a GO command, when it shouldn't	#

import sys
import threading
from roverpacket import *
from bus import *

class JoyParser(object):
	def __init__(self, bus, joy_queue):
		# Initializes threading
		threading.Thread.__init__(self)
		# Stores the bus object
		self.bus = bus
		self.joy_queue = queue
		# Creates lists and dictionaries
		self.templist = []
		self.joy_254 = {}
		self.joy_127 = {}
		self.joymap_counter_254 = float(0.00)
		self.joymap_counter_127 = float(0.00)
		self.left_wheel_ids = [2, 3, 4] # Front to Back
		self.right_wheel_ids = [5, 6, 7] # Front to Back
		self.tripod_id = 8
		self.arm_id = 9
		self.buttons = {'\x00':'A', '\x01':'B', '\x02':'X', '\x03':'Y', \
                                '\x04':'LB', '\x05':'RB', '\x06':'Back', '\x07':'Start', \
                                '\x08':'Middle', '\t':'LJ/Button', '\n':'RJ/Button'}
		# Initializes lists and dictionaries
		for x in range(8):
		        self.templist.append(0)
		for x in range(0,255):
		        self.joy_254[x] = float(self.joymap_counter_254)
		        self.joymap_counter_254 += float(0.390625)
		for x in range(0,128):
		        self.joy_127[x] = float(self.joymap_counter_127)
		        self.joymap_counter_127 += float(0.7874015748)

	def run(self):
		# Reads from bus.joy_rover
		# Parses info coming from there
		# Figures out the info for 6 packets each
		# Info needed: <addr> <motor_addr> <speed>
		# SEND BogiePacket 6 packets each time, it expects the previous info
		
		# Give Listener a list of 6 lists with the info needed

		# Initialize by sending all 0 commands

		# Start Parser
		while 1:
			# Returns list
			# for buttons,
			# for joy, list of 6 tuples, each holding <addr 2-7> <motor_addr> <speed> <angle>
			pressed_button = 0
			pressed_joy = 0
			released_button = 0
			info_list = []
			found = 0 # Just slightly speeds things up, no needs to parse info that has been parsed

			# Read 1 byte
			for x in range(8):
				self.templist[x] = self.bus.joy_rover.read(1)
		
			# BUTTON is PRESSED
			if self.templist[4]=='\x01' or self.templist[4]=='\xFF':
				found = 1
				pressed_button = self.parse_pressed_button() # Grab the return here
				if pressed_button is not None:
					info_list = translate_button(pressed_button)
				# If else, do nothing
				
			# JOYSTICK is PRESSED
			elif found==0:
				pressed_joy = self.parse_pressed_joy() # Grab the return
				if pressed_joy is not None:
					found = 1
					info_list = translate_joy(pressed_joy)
				# If else, do nothing

			# BUTTON is RELEASED
			elif self.templist[4]=='\x00' and found==0:
				released_button = self.parse_released() # Grab the return here
				if released_button is not None:
					info_list = translate_button(released_button)
				
			# Return list if there is a list to return
			if info_list is None:
				info_list = None # Do nothing
			else:
				self.joy_queue.put(info_list)
	
	def translate_button(self, button_data):
		# Returns list
		# for wheels, 6 lists, each holding <addr 2-7> <motor_addr> <speed>
		# for else, 
		name = button_data[0]
		data = button_data[1]
		info_list = []
		
		# Tripod Controls
		if name=='Left':
			thing = 0 # Do
		elif name=='Right':
			thing = 0 # Do
		elif name=='Up':
			thing = 0 # Do
		elif name=='Down':
			thing = 0 # Do
		
		# Does something
		elif name=='A':
			thing = 0 # Do
		elif name=='B':
			thing = 0 # Do
		elif name=='X':
			thing = 0 # Do
		elif name=='Y':
			thing = 0 # Do
			
		# Actuation Controls - Example: <addr 2-7> <2> <speed>
		# Assuming that Reverse is Left and Forward is Right
		elif name=='LB':
			# All Motor 2's Reverse at 5% speed
			for wheel_id in self.left_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 2, 0
					info_list.append(data_tuple)
				else:
					speed = data + 100 # +100 makes reverse
					data_tuple = wheel_id, 2, speed
					info_list.append(data_tuple)
			for wheel_id in self.right_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 2, 0
					info_list.append(data_tuple)
				else:
					speed = data + 100 # +100 makes reverse
					data_tuple = wheel_id, 2, speed
					info_list.append(data_tuple)
		elif name=='RB':
			# All Motor 2's Forward at 5% speed
			for wheel_id in self.left_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 2, 0
					info_list.append(data_tuple)
				else:
					speed = data # makes forward # redundant, but human readable
					data_tuple = wheel_id, 2, speed
					info_list.append(data_tuple)
			for wheel_id in self.right_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 2, 0
					info_list.append(data_tuple)
				else:
					speed = data # makes forward # redundant, but human readable
					data_tuple = wheel_id, 2, speed
					info_list.append(data_tuple)
			
		# Does Something
		elif name=='Back':
			thing = 0 # Do
		elif name=='Start':
			thing = 0 # Do
		elif name=='Middle': # Emergency Stop EVERYTHING?
			thing = 0 # Do
		elif name=='LJ/Button':
			thing = 0 # Do
		elif name=='RJ/Button':
			thing = 0 # Do
		
	def translate_joy(self, joy_data):
		# Returns list of 6 lists, each holding <addr 2-7> <motor_addr> <speed>
		# NOTE: Speed is always rounded down to nearest number
		name = joy_data[0]
		data = int(joy_data[1]) # Rounded down
		info_list = []
		
		# LT and RT just skid steer in place - Example: <addr 2-7> <1> <speed>
		if name=='LT':
			# Left wheels Reverse, Right wheels Forward
			for wheel_id in self.left_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 1, 0
					info_list.append(data_tuple)
				else:
					speed = data + 100 # +100 makes reverse
					data_tuple = wheel_id, 1, speed
					info_list.append(data_tuple)
			for wheel_id in self.right_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 1, 0
					info_list.append(data_tuple)
				else:
					speed = data # makes forward # redundant, but human readable
					data_tuple = wheel_id, 1, speed
					info_list.append(data_tuple)
		elif name=='RT':
			# Left wheels Forward, Right wheels Reverse
			for wheel_id in self.left_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 1, 0
					info_list.append(data_tuple)
				else:
					speed = data # makes forward # redundant, but human readable
					data_tuple = wheel_id, 1, speed
					info_list.append(data_tuple)
			for wheel_id in self.right_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 1, 0
					info_list.append(data_tuple)
				else:
					speed = data + 100 # +100 makes reverse
					data_tuple = wheel_id, 1, speed
					info_list.append(data_tuple)
					
		# LJ for Left Wheels - # Example: <addr 2-7> <1> <speed>
		elif name=='LJ/Right' or name=='LJ/Left':
			info_list = None
		elif name=='LJ/Up':
			# data is fine unchanged because 0-100 are forward values
			for wheel_id in self.left_wheel_ids:
				data_tuple = wheel_id, 1, data
				info_list.append(data_tuple)
				
		elif name=='LJ/Down':
			# data is changed because 0 and 101-200 are reverse values
			for wheel_id in self.left_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 1, 0
					info_list.append(data_tuple)
				else:
					speed = data + 100 # +100 makes reverse
					data_tuple = wheel_id, 1, speed
					info_list.append(data_tuple)
			
		# RJ for Right wheels - Example: <addr 2-7> <1> <speed>
		elif name=='RJ/Right' or name=='RJ/Left':
			info_list = None
		elif name=='RJ/Up':
			# data is fine unchanged because 0-100 are forward values
			for wheel_id in self.right_wheel_ids:
				data_tuple = wheel_id, 1, data
				info_list.append(data_tuple)
		elif name=='RJ/Down':
			# data is changed because 0 and 101-200 are reverse values
			for wheel_id in self.right_wheel_ids:
				if data==0:
					data_tuple = wheel_id, 1, 0
					info_list.append(data_tuple)
					self.previous_LJ_Down = 0
				else:
					speed = data + 100 # +100 makes reverse
					data_tuple = wheel_id, 1, speed
					info_list.append(data_tuple)
					self.previous_LJ_Down = speed
		return info_list
			
	
	def parse_pressed_button(self):
		# Returns list in format ["button", 1(on)]
		if self.templist[6]=='\x01' and self.templist[5]=='\x00': # Letters, Start/Back or LJ/RJ Buttons
			return [self.buttons[self.templist[7]], 1]
		elif self.templist[6]=='\x02' and self.templist[5]=='\x80': # D-Pad L/U
			if self.templist[7]=='\x06': # Left
				return ["Left", 1]
			elif self.templist[7]=='\x07': # Up
				return ["Up", 1]
		elif self.templist[6]=='\x02' and self.templist[5]=='\x7F': # D-Pad R/D
			if self.templist[7]=='\x06': # Right
				return ["Right", 1]
			elif self.templist[7]=='\x07': # Down
				return ["Down", 1]
		else:
			return None

	def parse_pressed_joy(self):
		# Returns list in format ["joy", amount 0.00-100.00]
		if self.templist[7]=='\x02' and self.templist[6]=='\x02': # LT
			if ord(self.templist[5])>=128:
				val = "%.2f" % self.joy_254[ord(self.templist[5]) - 128]
				return ["LT", val]
			elif ord(self.templist[5])<=127:
				val = "%.2f" % self.joy_254[ord(self.templist[5]) + 127]
				return ["LT", val]
		elif self.templist[7]=='\x05' and self.templist[6]=='\x02': # RT
			if ord(self.templist[5])>=128:
				val = "%.2f" % self.joy_254[ord(self.templist[5]) - 128]
				return ["RT", val]
			elif ord(self.templist[5])<=127:
				val = "%.2f" % self.joy_254[ord(self.templist[5]) + 127]
				return ["RT", val]
		elif self.templist[7]=='\x00' and self.templist[6]=='\x02': # Left-Joy L/R
			if ord(self.templist[5])<=127: # Right
				val = "%.2f" % self.joy_127[ord(self.templist[5])]
				return ["LJ/Right", val]
			elif ord(self.templist[5])>=128: # Left
				val = "%.2f" % self.joy_127[abs(ord(self.templist[5]) - 254)]
				return ["LJ/Left", val]
		elif self.templist[7]=='\x01' and self.templist[6]=='\x02': # Left-Joy U/D
			if ord(self.templist[5])<=127: # Down
				val = "%.2f" % self.joy_127[ord(self.templist[5])]
				return ["LJ/Down", val]
			elif ord(self.templist[5])>=128: # Up
				val = "%.2f" % self.joy_127[abs(ord(self.templist[5]) - 254)]
				return ["LJ/Up", val]
		elif self.templist[7]=='\x03' and self.templist[6]=='\x02': # Right-Joy L/R
			if ord(self.templist[5])<=127: # Right
				val = "%.2f" % self.joy_127[ord(self.templist[5])]
				return ["RJ/Right", val]
			elif ord(self.templist[5])>=128: # Left
				val = "%.2f" % self.joy_127[abs(ord(self.templist[5]) - 254)]
				return ["RJ/Left", val]
		elif self.templist[7]=='\x04' and self.templist[6]=='\x02': # Right-Joy U/D
			if ord(self.templist[5])<=127: # Down
				val = "%.2f" % self.joy_127[ord(self.templist[5])]
				return ["RJ/Down", val]
			elif ord(self.templist[5])>=128: # Up
				val = "%.2f" % self.joy_127[abs(ord(self.templist[5]) - 254)]
				return ["RJ/Up", val]
		else:
			return None


	def parse_released(self):
		# Returns list in format ["button/joy", 0(off)]
		if self.templist[5]=='\x00': # Letters, Start/Stop, or LJ/RJ Buttons
			return [self.buttons[self.templist[7]], 0]
		elif self.templist[5]=='\x80': # D-Pad, Left/Up
			if self.templist[7]=='\x06': # Left
				return ["Left", 0]
			elif self.templist[7]=='\x07': # Up
				return ["Up", 0]
		elif self.templist[5]=='\x7F': # D-Pad, Right/Down
			if self.templist[7]=='\x06': # Right
				return ["Right", 0]
			elif self.templist[7]=='\x07': # Down
				return ["Down", 0]
		else:
			return None
		