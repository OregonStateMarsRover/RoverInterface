############ XBox Controller Parser - joy_core.py ##########
# Original Author: John Zeller
# Description: Joy_Core parses data coming from the Xbox controller and updates a
#	       dictionary of states.

### NOTES ###############################################################################
# 1) LEAVE MODE 'OFF' there is no support in joy.py for MODE ON 			#
# 2) This parser was built using this tutorial as a reference:				#
#	http://hackshark.com/?p=147#axzz2BHTVXCFz					#
# 3) Naturally the gamepad sends the following values:					#
# 	LJ/RJ - Down: 0-127								#
# 	LJ/RJ - Up: 255-128								#
# 	LJ/RJ - Left: 255-128								#
# 	LJ/RJ - Right: 0-127								#
#########################################################################################

### Current Abilities ###################################################################
# Skid Steering										#
# 	LJ - Controls all left wheels forward/reverse (no left/right) 			#
# 	RJ - Controls all right wheels forward/reverse (no left/right)			#
# 	LT - Throttles a 0-point skid steer to the left					#
# 	RT - Throttles a 0-point skid steer to the right				#
# 	Y - Software Mode Change (Skid to Vector Steering)				#
# Vector Steering									#
# 	LJ - Controls all left wheels forward/reverse (no left/right) 			#
# 	RJ - Controls the set angle for actuation. (no down)				#
# 	Y - Software Mode Change (Skid to Vector Steering)				#
#########################################################################################

### Buttons/Joys Represented: ###########################################################
# A, B, X, Y, RB, LB, LJButton, RJButton, Back, Start, Middle				#
# RT, LT, LeftJoy, RightJoy, Left, Right, Up, Down					#
#########################################################################################

### Need To Implement: ##################################################################
# 1) When the Joy hits back to 0, then send a 0 speed command... sometimes it ends with	#
#    a speed value other than 0								#
# 2) Check the values of the Trigger and Joy released packets and have that send a stop #
#    command...currently not robust to never receiving a 0 command from joy		#
# 3) RJ - Vector Steer Mode - translate_joy						#
# 4) D-Pad - Tripod Controls								#
# 5) Middle - Emergency Stop All Systems						#
#########################################################################################

### States Reference: ###################################################################
#	self.states = { 'A':0, 'B':0, 'X':0, 'Y':0,  		   		\	#
#			'Back':0, 'Start':0, 'Middle':0,		   	\	#
#			'Left':0, 'Right':0, 'Up':0, 'Down':0, 			\	#
#			'LB':0, 'RB':0, 'LT':0, 'RT':0,				\	#
#			'Control_Scheme':0,					\	#
#			'LJ/Button':0, 'RJ/Button':0, 				\	#
#			'LJ/Left':0, 'LJ/Right':0, 'LJ/Up':0, 'LJ/Down':0, 	\	#
#			'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0,	\	#
#			'skid_right_trigger':0, 'skid_left_trigger':0, 		\	#
#			'skid_right_joy':0, 'skid_left_joy':0, 			\	#
#			'vector_right_trigger':0, 'vector_left_trigger':0,	\	#
#			'vector_right_joy_RightLeft':0, 			\	#
#			'vector_right_joy_Up':0, 'vector_left_joy':0}			#
#########################################################################################

### TODO IMMEDIATELY: ###################################################################
# 1) Line 126: In self.clean_states(), figure out why the trigger states need changing	#
#    this is something that only joy_core should be doing, but right now it seems wheel	#
#    specific										#
#########################################################################################

import sys
import threading
from bus import *

class JoyParser(threading.Thread):
	def __init__(self, bus, states):
		# Initializes threading
		threading.Thread.__init__(self)
		# Stores the bus and states objects
		self.bus = bus
		self.states = states
		# Creates lists and dictionaries
		self.templist = []
		self.left_wheel_ids = [2, 3, 4] # Front to Back
		self.right_wheel_ids = [5, 6, 7] # Front to Back
		self.tripod_id = 8
		self.arm_id = 9
		# Tracks the press of 'Y' which changes control from Skid to Vector
		self.states['Control_Scheme'] = 0
		# All button raw packet values of data coming from gamepad
		self.buttons = {'\x00':'A', '\x01':'B', '\x02':'X', '\x03':'Y', \
				'\x04':'LB', '\x05':'RB', '\x06':'Back', '\x07':'Start', \
				'\x08':'Middle', '\t':'LJ/Button', '\n':'RJ/Button'}
		# Initializes templist
		for x in range(8):
		        self.templist.append(0)

	def run(self):
		# Start Parser
		while 1:
			pressed_button = 0
			pressed_joy = 0
			released_button = 0
			found = 0 # Just slightly speeds things up, no need to parse info that has been parsed

			# Read 1 byte
			for x in range(8):
				self.templist[x] = self.bus.joy_rover.read(1)
		
			# BUTTON is PRESSED
			if self.templist[4]=='\x01' or self.templist[4]=='\xFF':
				found = 1
				pressed_button = self.parse_pressed_button() # Grab the return here
				if pressed_button is not None:
					if pressed_button[0]=='Y' and self.states['Control_Scheme']==0:
						# Control Scheme for Vector
						self.states['Control_Scheme'] = 1
					elif pressed_button[0]=='Y' and self.states['Control_Scheme']==1:
						# Control Scheme for Skid
						self.states['Control_Scheme'] = 0
					# If else, do nothing
				# If else, do nothing
				
			# JOYSTICK is PRESSED
				# Description: 	parse_pressed_joy parses the raw data coming from joystick
				#		translate_joy figures out what that data means and sets global variables
			elif found==0:
				pressed_joy = self.parse_pressed_joy() # Grab the return
				if pressed_joy is not None:
					found = 1
					self.translate_joy(pressed_joy)
				# If else, do nothing

			# BUTTON is RELEASED
			elif self.templist[4]=='\x00' and found==0:
				released_button = self.parse_released() # Grab the return here
					
			# Clean States, regardless
			self.clean_states()

	def clean_states(self):
		# Looks at the states in the dictionary and adjusts for things like boundary values
		# 	making them safer (ie if joy passes 1 when it means 0, just adjust to 0)
		if self.states['Control_Scheme'] == 0:
			# LT and RT just skid steer in place - Example: <addr 2-7> <speed> <0>
			# For RT - Left wheels Forward, Right wheels Reverse
			if self.states['skid_left_joy'] == 0 and self.states['skid_right_joy'] == 0:
				for wheel_id in self.left_wheel_ids:
					if self.states['skid_right_trigger']!=0: # Forward (255-128)
						speed = self.states['skid_right_trigger'] / 2 - 1 # Down 1 to ensure a 0 value
						if speed == 0:
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
						if speed < 0:				# Checks to ensure no negatives
							speed = 0
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
				for wheel_id in self.right_wheel_ids:
					if self.states['skid_right_trigger']!=0: # Reverse
						speed = -(self.states['skid_right_trigger'] / 2 - 1) # Down 1 to ensure a 0 value
						if speed == 0:
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
						if speed > 0:				# Checks to ensure no positives
							speed = 0
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
	
	def translate_button(self, button_data):
		# Returns list
		# for wheels, 6 lists, each holding <addr 2-7> <speed> <angle>
		# for else, 
		name = button_data[0]
		data = button_data[1]
		
		# Tripod Controls
		if name=='Left':
			self.states['Left'] = 0 # Do nothing
		elif name=='Right':
			self.states['Right'] = 0 # Do nothing
		elif name=='Up':
			self.states['Up'] = 0 # Do nothing
		elif name=='Down':
			self.states['Down'] = 0 # Do nothing
		
		# Does something
		elif name=='A':
			self.states['A'] = 0 # Do nothing
		elif name=='B':
			self.states['B'] = 0 # Do nothing
		elif name=='X':
			self.states['X'] = 0 # Do nothing
		# elif name=='Y': <-- Checked in def run already
			
		elif name=='LB':
			self.states['LB'] = 0 # Do nothing
		elif name=='RB':
			self.states['RB'] = 0 # Do nothing
			
		# Does Something
		elif name=='Back':
			self.states['Back'] = 0 # Do nothing
		elif name=='Start':
			self.states['Start'] = 0 # Do nothing
		elif name=='Middle': # Emergency Stop EVERYTHING?
			self.states['Middle'] = 0 # Do nothing
		elif name=='LJ/Button':
			self.states['LJ/Button'] = 0 # Do nothing
		elif name=='RJ/Button':
			self.states['RJ/Button'] = 0 # Do nothing
		
	def translate_joy(self, joy_data):
		# Instead of returning info, sets states of joy global variables
		name = joy_data[0]
		data = joy_data[1]
		
		# Skid Steer Mode
		if self.states['Control_Scheme']==0:
			# LT and RT just skid steer in place
			if name=='LT':
				# Left wheels Reverse, Right wheels Forward
				self.states['skid_left_trigger'] = int(data)
				nothing = 0 # Do nothing
			elif name=='RT':
				# Left wheels Forward, Right wheels Reverse
				self.states['skid_right_trigger'] = int(data)
				nothing = 0 # Do nothing
						
			# LJ for Left Wheels
			elif name=='LJ/Right' or name=='LJ/Left':
				nothing = 0 # Do nothing
			elif name=='LJ/Up' or name=='LJ/Down':
				self.states['skid_left_joy'] = -(int(data))	# Flip the sign value, because it is backwards
				
			# RJ for Right wheels
			elif name=='RJ/Right' or name=='RJ/Left':
				nothing = 0 # Do nothing
			elif name=='RJ/Up' or name=='RJ/Down':
				self.states['skid_right_joy'] = -(int(data))	# Flip the sign value, because it is backwards
					
					
		# Vector Steer Mode
		elif self.states['Control_Scheme']==1:
			if name=='LT':
				nothing = 0 # Do nothing
			elif name=='RT':
				nothing = 0 # Do nothing
				
			# LJ for Drive Forward/Reverse
			elif name=='LJ/Right' or name=='LJ/Left':
				nothing = 0 # Do nothing
			elif name=='LJ/Up' or name=='LJ/Down':
				self.states['vector_left_joy'] = -(int(data))	# Flip the sign value, because it is backwards

			# RJ for Angle from 0-180 (0 starts at -90) - Example: <addr 2-7> <0> <angle>
			# Calculate the x and y-components of this to compute the angle
			elif name=='RJ/Right' or name=='RJ/Left':
				self.states['vector_right_joy_RightLeft'] = int(data)
			elif name=='RJ/Up':
				self.states['vector_right_joy_Up'] = -(int(data))	# Flip the sign value, because it is backwards
			elif name=='RJ/Down':
				nothing = 0 # Do nothing
	
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
		