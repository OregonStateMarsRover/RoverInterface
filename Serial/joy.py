############ XBox Controller Parser - joy.py ##########

# Original Author: John Zeller

# Joy parses data coming from the Xbox controller and adds it to joy_queue
# Listener is listening to what Joy places into this queue and will package
# and send the appropriate information to the receptionist

### Left to Implement ###################################################
# RJ - Vector Steer Mode - translate_joy				#

### Abilities - Skid Steering ###########################################
# LJ - Controls all left wheels forward/reverse (no left/right) 	#
# RJ - Controls all right wheels forward/reverse (no left/right)	#
# LT - Throttles a 0-point skid steer to the left			#
# RT - Throttles a 0-point skid steer to the right			#
# Y - Software Mode Change (Skid to Vector Steering)			#
#########################################################################

### Abilities - Vector Steering #########################################
# LJ - Controls all left wheels forward/reverse (no left/right) 	#
# RJ - Controls the set angle for actuation. (no down)			#
# Y - Software Mode Change (Skid to Vector Steering)			#
#########################################################################

### Soon-to-come Abilities ##############################################
# D-Pad - Tripod Controls						#
# Middle - Emergency Stop All Systems					#
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

# Variables for RT, LT, RJ, LJ


import sys
import threading
from roverpacket import *
from bus import *

class JoyParser(threading.Thread):
	def __init__(self, bus, joy_queue):
		# Initializes threading
		threading.Thread.__init__(self)
		# Stores the bus object
		self.bus = bus
		self.joy_queue = joy_queue
		# Creates lists and dictionaries
		self.templist = []
		self.left_wheel_ids = [2, 3, 4] # Front to Back
		self.right_wheel_ids = [5, 6, 7] # Front to Back
		self.tripod_id = 8
		self.arm_id = 9
		# Tracks the press of 'Y' which changes control from Skid to Vector
		self.control_change = 0
		self.buttons = {'\x00':'A', '\x01':'B', '\x02':'X', '\x03':'Y', \
                                '\x04':'LB', '\x05':'RB', '\x06':'Back', '\x07':'Start', \
                                '\x08':'Middle', '\t':'LJ/Button', '\n':'RJ/Button'}
		# State dictionary to track previous values for all gamepad actions
		self.states = {'A':0, 'B':0, 'X':0, 'Y':0, 'LB':0, 'RB':0,  \
				'Back':0, 'Start':0, 'LJ/Button':0, 'RJ/Button':0, \
				'Middle':0, 'Left':0, 'Right':0, 'Up':0, 'Down':0, \
				'LJ/Left':0, 'LJ/Right':0, 'LJ/Up':0, 'LJ/Down':0, \
				'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0}
		# Initializes templist
		for x in range(8):
		        self.templist.append(0)
		# Joy - States
		self.right_trigger = 0
		self.left_trigger = 0
		self.right_joy = 0
		self.left_trigger = 0

	def run(self):
		# Figures out the info for 6 packets each
		# Info needed: <addr> <motor_addr> <speed>
		# SEND BogiePacket 6 packets each time, it expects the previous info
		
		# Give Listener a list of 6 lists with the info needed

		# Initialize by sending all 0 commands

		# Start Parser
		while 1:
			# Returns list
			# for buttons,
			# for joy, list of 6 tuples, each holding <addr 2-7> <speed> <angle>
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
					if pressed_button[0]=='Y' and self.control_change==0:
						# Control Scheme for Vector
						self.control_change = 1
					elif pressed_button[0]=='Y' and self.control_change==1:
						# Control Scheme for Skid
						self.control_change = 0
					else:
						info_list = self.translate_button(pressed_button)
				# If else, do nothing
				
			# JOYSTICK is PRESSED
			elif found==0:
				pressed_joy = self.parse_pressed_joy() # Grab the return
				if pressed_joy is not None:
					found = 1
					info_list = self.translate_joy(pressed_joy)
				# If else, do nothing

			# BUTTON is RELEASED
			elif self.templist[4]=='\x00' and found==0:
				released_button = self.parse_released() # Grab the return here
				if released_button is not None:
					info_list = self.translate_button(released_button)
				
			# Return list if there is a list to return
			if info_list is None:
				info_list = None # Do nothing
			else:
				self.joy_queue.put(info_list)
	
	def translate_button(self, button_data):
		# Returns list
		# for wheels, 6 lists, each holding <addr 2-7> <speed> <angle>
		# for else, 
		name = button_data[0]
		data = button_data[1]
		info_list = []
		
		# Tripod Controls
		if name=='Left':
			info_list = None
		elif name=='Right':
			info_list = None
		elif name=='Up':
			info_list = None
		elif name=='Down':
			info_list = None
		
		# Does something
		elif name=='A':
			info_list = None
		elif name=='B':
			info_list = None
		elif name=='X':
			info_list = None
		# elif name=='Y': <-- Checked in def run already
			
		elif name=='LB':
			info_list = None
		elif name=='RB':
			info_list = None
			
		# Does Something
		elif name=='Back':
			info_list = None
		elif name=='Start':
			info_list = None
		elif name=='Middle': # Emergency Stop EVERYTHING?
			info_list = None
		elif name=='LJ/Button':
			info_list = None
		elif name=='RJ/Button':
			info_list = None
			
		return info_list
		
	def translate_joy(self, joy_data):
		# Returns list of 6 lists, each holding <addr 2-7> <speed> <angle>
		# NOTE: Speed is for drive, angle is for actuation
		name = joy_data[0]
		data = joy_data[1]
		info_list = []
		
		# Skid Steer Mode
		if self.control_change==0:
			# LT and RT just skid steer in place - Example: <addr 2-7> <speed> <0>
			if name=='LT':
				# Left wheels Reverse, Right wheels Forward
				for wheel_id in self.left_wheel_ids:
					if data==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Reverse (0-127)
						data = int(data) / 2 # Round down
						data_tuple = wheel_id, data, 0
						info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					if data==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Forward (255-128)
						data = int(data) / 2 + 128 # Round down
						data_tuple = wheel_id, data, 0
						info_list.append(data_tuple)
			elif name=='RT':
				# Left wheels Forward, Right wheels Reverse
				for wheel_id in self.left_wheel_ids:
					if data==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Reverse (0-127)
						data = int(data) / 2 + 128 # Round down
						data_tuple = wheel_id, data, 0
						info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					if data==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Forward (255-128)
						data = int(data) / 2 # Round down
						data_tuple = wheel_id, data, 0
						info_list.append(data_tuple)
						
			# LJ for Left Wheels - # Example: <addr 2-7> <speed> <0>
			elif name=='LJ/Right' or name=='LJ/Left':
				info_list = None
			elif name=='LJ/Up' or name=='LJ/Down':
				for wheel_id in self.left_wheel_ids:
					data_tuple = wheel_id, data, 0
					info_list.append(data_tuple)
				
			# RJ for Right wheels - Example: <addr 2-7> <speed>
			elif name=='RJ/Right' or name=='RJ/Left':
				info_list = None
			elif name=='RJ/Up' or name=='RJ/Down':
				for wheel_id in self.right_wheel_ids:
					data_tuple = wheel_id, data, 0
					info_list.append(data_tuple)
					
					
		# Vector Steer Mode
		elif self.control_change==1:
			if name=='LT':
				info_list = None
			elif name=='RT':
				info_list = None
				
			# LJ for Drive Forward/Reverse - # Example: <addr 2-7> <speed> <0> for ALL 6 wheels at once
			elif name=='LJ/Right' or name=='LJ/Left':
				info_list = None
			elif name=='LJ/Up' or name=='LJ/Down':
				for wheel_id in self.left_wheel_ids:
					data_tuple = wheel_id, data, 0
					info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					data_tuple = wheel_id, data, 0
					info_list.append(data_tuple)

			# RJ for Angle from 0-180 (0 starts at -90) - Example: <addr 2-7> <0> <angle>
			# Calculate the x and y-components of this to compute the angle
			elif name=='RJ/Right' or name=='RJ/Left':
				info_list = None
			elif name=='RJ/Up' or name=='RJ/Down':
				info_list = None
				
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
		# Returns list in format ["joy", amount 0-255]
		if self.templist[7]=='\x02' and self.templist[6]=='\x02': # LT
			if ord(self.templist[5])>=128:
				val = str(ord(self.templist[5]) - 128)
				return ["LT", val]
			elif ord(self.templist[5])<=127:
				val = str(ord(self.templist[5]) + 127)
				return ["LT", val]
		elif self.templist[7]=='\x05' and self.templist[6]=='\x02': # RT
			if ord(self.templist[5])>=128:
				val = str(ord(self.templist[5]) - 128)
				return ["RT", val]
			elif ord(self.templist[5])<=127:
				val = str(ord(self.templist[5]) + 127)
				return ["RT", val]
		elif self.templist[7]=='\x00' and self.templist[6]=='\x02': # Left-Joy L/R
			if ord(self.templist[5])<=127: # Right
				val = str(ord(self.templist[5]))
				return ["LJ/Right", val]
			elif ord(self.templist[5])>=128: # Left
				val = str(ord(self.templist[5]))
				return ["LJ/Left", val]
		elif self.templist[7]=='\x01' and self.templist[6]=='\x02': # Left-Joy U/D
			if ord(self.templist[5])<=127: # Down
				val = str(ord(self.templist[5]))
				return ["LJ/Down", val]
			elif ord(self.templist[5])>=128: # Up
				val = str(ord(self.templist[5]) - 255)
				return ["LJ/Up", val]
		elif self.templist[7]=='\x03' and self.templist[6]=='\x02': # Right-Joy L/R
			if ord(self.templist[5])<=127: # Right
				val = str(ord(self.templist[5]))
				return ["RJ/Right", val]
			elif ord(self.templist[5])>=128: # Left
				val = str(ord(self.templist[5]) - 255)
				return ["RJ/Left", val]
		elif self.templist[7]=='\x04' and self.templist[6]=='\x02': # Right-Joy U/D
			if ord(self.templist[5])<=127: # Down
				val = str(ord(self.templist[5]))
				return ["RJ/Down", val]
			elif ord(self.templist[5])>=128: # Up
				val = str(ord(self.templist[5]) - 255)
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
		