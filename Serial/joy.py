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

#### Note on LJ/RJ values: ######################################
# Naturally the gamepad sends the following values:		#
# LJ/RJ - Down: 0-127						#
# LJ/RJ - Up: 255-128						#
# LJ/RJ - Left: 255-128						#
# LJ/RJ - Right: 0-127						#
#################################################################

#### Possible Additions: ################################################################
# 1) When the Joy hits back to 0, then send a 0 speed command... sometimes it ends with	#
#    a speed value other than 0								#
# 2) In case of artifacts in serial communication, initialize communication with all 0	#
#    values for speeds, just in case the rover is given a GO command, when it shouldn't	#


# Need to implement
# 	Create variables for RT, LT, RJ and LJ
# 	Have a translate_joy set the values of these gloval variables
# 	Have another algorithm reading the info from these variables and assembling tuples from there
# ************Check the values of the Trigger and Joy released packets and have that send a stop command...
#			currently not robust to never receiving a 0 command from joy


# 	Change Left and Right speeds to be mirrors of each other. This is because the wheels are mirrors


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
		# All button raw packet values of data coming from gamepad
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
		# Joy - States (Joys only have up/down values, Triggers only have forward values)
			# These are always integer values
		self.skid_right_trigger = 0
		self.skid_left_trigger = 0
		self.skid_right_joy = 0
		self.skid_left_joy = 0
		self.vector_right_trigger = 0
		self.vector_left_trigger = 0
		self.vector_right_joy_RightLeft = 0
		self.vector_right_joy_Up = 0
		self.vector_left_joy = 0

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
				# Explanation: 	parse_pressed_joy parses the raw data coming from joystick
				#		translate_joy figures out what that data means and sets global variables
				#		design_commands_joy looks at the global variables that have been set and
				#			returns a list of 6 tuples for use by listener
			elif found==0:
				pressed_joy = self.parse_pressed_joy() # Grab the return
				if pressed_joy is not None:
					found = 1
					self.translate_joy(pressed_joy)
					info_list = self.design_commands_joy()
				# If else, do nothing

			# BUTTON is RELEASED
			elif self.templist[4]=='\x00' and found==0:
				released_button = self.parse_released() # Grab the return here
				if released_button is not None:
					info_list = self.translate_button(released_button)
				
			# Return list if there is a list to return, otherwise do nothing
			if info_list is None:
				info_list = None # Do nothing
			else:
				self.joy_queue.put(info_list)
	
	# Within design_commands_joy
	#
	# Working: RT, LT, RJ/LJ
	#
	# Needs work: Vector RJ for angles
	def design_commands_joy(self):
		info_list = []
		# Look at each of the values for variables skid_right_trigger, skid_left_trigger, skid_right_joy, skid_left_joy
		# 	and figure out the appropriate commands to send for all 6 wheels
		# Returns a list of 6 tuples with the format Example: <addr 2-7> <speed> <angle>
		#	speed being for skid, and angle being for vector
		# Be mindful of the self.control_change with 0 being skid, and 1 being vector
		
		# Right of Way - Skid Steer
		# 	LJ/RJ (Both because they don't have overcrossing commands)
		# 	RT - ONLY ALLOW if LJ/RJ are 0
		# 	LT - ONLY ALLOW if LJ/RJ and RT are 0
		# Right of Way - Vector Steer
		# 	RJ - Allow the wheels to actuate before they drive
		#		(otherwise you may get some drive packets and some angle packets intermingled with each other)
		# 	LJ - ONLY ALLOW if RJ is at 0 OR IF THE ANGLE HAS BEEN HELD
		# ORRRRRRRRR
		# 	LJ/RJ (Both because they don't have overcrossing commands)
		# Always allow zeros to be sent
		
		# Skid Steer Mode
		if self.control_change == 0:
			# LJ and RJ are setup using the tank drive concept - # Example: <addr 2-7> <speed> <0>
			# LJ for Left Wheels (Forward/Reverse)
			for wheel_id in self.left_wheel_ids:
				data_tuple = wheel_id, self.skid_left_joy, 0
				info_list.append(data_tuple)
			# RJ for Right Wheels (Forward/Reverse)
			for wheel_id in self.right_wheel_ids:
				data_tuple = wheel_id, self.skid_right_joy, 0
				info_list.append(data_tuple)
			
			# LT and RT just skid steer in place - Example: <addr 2-7> <speed> <0>
			# For RT - Left wheels Forward, Right wheels Reverse
			if self.skid_left_joy == 0 and self.skid_right_joy == 0:
				info_list = []	# If LJ/RJ were already 0, then go ahead with RT commands
				for wheel_id in self.left_wheel_ids:
					if self.skid_right_trigger==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Forward (255-128)
						speed = self.skid_right_trigger / 2 - 1 # Down 1 to ensure a 0 value
						if speed == 0:
							self.skid_right_trigger = 0	# Ensures that right trigger is 0
						if speed < 0:				# Checks to ensure no negatives
							speed = 0
							self.skid_right_trigger = 0	# Ensures that right trigger is 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					if self.skid_right_trigger==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Reverse
						speed = -(self.skid_right_trigger / 2 - 1) # Down 1 to ensure a 0 value
						if speed == 0:
							self.skid_right_trigger = 0	# Ensures that right trigger is 0
						if speed > 0:				# Checks to ensure no positives
							speed = 0
							self.skid_right_trigger = 0	# Ensures that right trigger is 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
			# For LT - Left wheels Reverse, Right wheels Forward
			if self.skid_left_joy == 0 and self.skid_right_joy == 0 and self.skid_right_trigger == 0:
				info_list = []	# If LJ/RJ and RT were already 0, then go ahead with RT commands
				for wheel_id in self.left_wheel_ids:
					if self.skid_left_trigger==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Reverse (0-127)
						speed = -(self.skid_left_trigger / 2 - 1) # Down 1 to ensure a 0 value
						if speed > 0:				# Checks to ensure no positives
							speed = 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					if self.skid_left_trigger==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Forward (255-128)
						speed = self.skid_left_trigger / 2 - 1 # Down 1 to ensure a 0 value
						if speed < 0:				# Checks to ensure no negatives
							speed = 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
			# If everything is already 0, then LT will be allowed to run, but will reset values to 0
						
		
		# Vector Steer Mode
		elif self.control_change == 1:
			# LJ for Left/Right Wheels (Forward/Reverse) - # Example: <addr 2-7> <speed> <0>
			for wheel_id in self.left_wheel_ids:
				data_tuple = wheel_id, self.vector_left_joy, 0
				info_list.append(data_tuple)
			for wheel_id in self.right_wheel_ids:
				data_tuple = wheel_id, self.vector_left_joy, 0
				info_list.append(data_tuple)
				
			# RJ for actuation, calculates an angle - # Example: <addr 2-7> <0> <angle>
			# The value ranges are:
			# 	RJ - Right: 0 to 127
			# 	RJ - Left: 0 to -127
			# 	RJ - Up: 0 to 127
			for wheel_id in self.left_wheel_ids:
				nothing = 0	# Do Nothing
			for wheel_id in self.right_wheel_ids:
				nothing = 0	# Do Nothing
				
				
			# Append info_list with values of RJ-RightLeft and RJ-Up
			info_list.append("RJ - RightLeft: ")
			info_list.append(self.vector_right_joy_RightLeft)
			info_list.append("RJ - Up")
			info_list.append(self.vector_right_joy_Up)
		
		return info_list
	
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
		# Instead of returning info, sets states of joy global variables
		name = joy_data[0]
		data = joy_data[1]
		info_list = []
		
		# Skid Steer Mode
		if self.control_change==0:
			# LT and RT just skid steer in place
			if name=='LT':
				# Left wheels Reverse, Right wheels Forward
				self.skid_left_trigger = int(data)
				info_list = None
			elif name=='RT':
				# Left wheels Forward, Right wheels Reverse
				self.skid_right_trigger = int(data)
				info_list = None
						
			# LJ for Left Wheels
			elif name=='LJ/Right' or name=='LJ/Left':
				info_list = None
			elif name=='LJ/Up' or name=='LJ/Down':
				self.skid_left_joy = -(int(data))	# Flip the sign value, because it is backwards
				
			# RJ for Right wheels
			elif name=='RJ/Right' or name=='RJ/Left':
				info_list = None
			elif name=='RJ/Up' or name=='RJ/Down':
				self.skid_right_joy = -(int(data))	# Flip the sign value, because it is backwards
					
					
		# Vector Steer Mode
		elif self.control_change==1:
			if name=='LT':
				info_list = None
			elif name=='RT':
				info_list = None
				
			# LJ for Drive Forward/Reverse
			elif name=='LJ/Right' or name=='LJ/Left':
				info_list = None
			elif name=='LJ/Up' or name=='LJ/Down':
				self.vector_left_joy = -(int(data))	# Flip the sign value, because it is backwards

			# RJ for Angle from 0-180 (0 starts at -90) - Example: <addr 2-7> <0> <angle>
			# Calculate the x and y-components of this to compute the angle
			elif name=='RJ/Right' or name=='RJ/Left':
				self.vector_right_joy_RightLeft = int(data)
			elif name=='RJ/Up':
				self.vector_right_joy_Up = -(int(data))	# Flip the sign value, because it is backwards
			elif name=='RJ/Down':
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
		