############ XBox Controller Poll'er - joy_main.py ##########
# Original Author: John Zeller
# Description: Joy_Main polls the data in a python dictionary to check the states of
# 	       several buttons coming from joy_core.py. Once it reads these states, it
#	       will decide what to do with the data, then pass it into a queue called,
#	       joy_queue

### NOTES ###############################################################################
# 1) LEAVE MODE 'OFF' there is no support in joy.py for MODE ON 			#
# 2) Naturally the gamepad sends the following values:					#
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
# 1) In case of artifacts in serial communication, initialize communication with all 0	#
#    values for speeds, just in case the rover is given a GO command, when it shouldn't	#
# 2) RJ - Vector Steer Mode								#
# 3) D-Pad - Tripod Controls								#
# 4) Middle - Emergency Stop All Systems						#
#########################################################################################

import sys
import threading
from bus import *
from joy_core import *

class JoyPoller(threading.Thread):
	def __init__(self, bus, joy_queue):
		# Initializes threading
		threading.Thread.__init__(self)
		# Stores the bus and joy_queue objects
		self.bus = bus
		self.joy_queue = joy_queue
		# Create a dictionary to be used to keep states from joy_core
		self.states = { 'A':0, 'B':0, 'X':0, 'Y':0,  		   		\
				'Back':0, 'Start':0, 'Middle':0,		   	\
				'Left':0, 'Right':0, 'Up':0, 'Down':0, 			\
				'LB':0, 'RB':0, 'LT':0, 'RT':0,				\
				'Control_Scheme':0,					\
				'LJ/Button':0, 'RJ/Button':0, 				\
				'LJ/Left':0, 'LJ/Right':0, 'LJ/Up':0, 'LJ/Down':0, 	\
				'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0,	\
				'skid_right_trigger':0, 'skid_left_trigger':0, 		\
				'skid_right_joy':0, 'skid_left_joy':0, 			\
				'vector_right_trigger':0, 'vector_left_trigger':0,	\
				'vector_right_joy_RightLeft':0, 			\
				'vector_right_joy_Up':0, 'vector_left_joy':0}
		# Lists of the names of buttons and joys - So we can iterate
		self.buttons = ['A', 'B', 'X', 'Y', 'Back', 'Start', 'Middle', 'Left', 	\
				'Right', 'Up', 'Down', 'LB', 'RB', 'LT', 'RT', 		\
				'LJ/Button', 'RJ/Button',]
		self.joys = ['LJ/Left', 'LJ/Right', 'LJ/Up', 'LJ/Down', 		\
			     'RJ/Left', 'RJ/Right', 'RJ/Up', 'RJ/Down', 		\
			     'skid_right_trigger', 'skid_left_trigger', 		\
			     'skid_right_joy', 'skid_left_joy', 			\
			     'vector_right_trigger', 'vector_left_trigger', 		\
			     'vector_right_joy_RightLeft', 'vector_right_joy_Up', 	\
			     'vector_left_joy']
		# Launch Joy_Core as a seperate thread to parse the joy
		self.joycore = JoyParser(self.bus, self.states)
		self.joycore.start()
		# Creates lists and dictionaries
		self.templist = []
		self.left_wheel_ids = [2, 3, 4] # Front to Back
		self.right_wheel_ids = [5, 6, 7] # Front to Back
		self.tripod_id = 8
		self.arm_id = 9
	
	def run(self):
		# Description: Calls the proper design commands for buttons and joys, which returns
		#	       the info needed for listener to have a packet assembled. This info is 
		#	       placed in the joy_queue for the listener.
		#	       Wheel info is placed in the joy_queue in the form of a list of 6 lists,
		#	       each with the format <addr> <motor_addr> <speed>.
		#	       Button info is placed in the joy_queue in the form of a single list,
		#	       each with the format <addr> <data>.
		#	       The Listener than
		#	       uses those info lists to send to RoverPacket for assembling it into
		#	       packets.
		
		# Start Poll'er
		while 1:
			# Questions: 1) How does joy_main know when a button is released, so that it can send a release packet? Or is our program release independent?
			#	     2) When an if triggers a return of design_commands, has the state already changed? Is it quick enough? Or do we need to pass in the state value?
				
			# BUTTON is PRESSED - Check if a button has been pressed by looking for 1's
			for button in self.buttons:
				if self.states[button] == 1:
					self.joy_queue.put(self.design_commands_button()) # Then design a button command and put it in the joy_queue
				
			# JOYSTICK is PRESSED
			self.joy_queue.put(self.design_commands_joy()) # Design a joy command and put it in the joy_queue
			
			# BUTTON is RELEASED - Necessary?	

	# Description: Looks at the button states and returns an into_list for use by the Listener
	# Needs Work: ALL Buttons
	def design_commands_button(self):
		nothing = 0 # Do Nothing for now
		
	# Description: Looks at the joy states and returns an info_list of 6 tuples for use by the Listener
	# Currently Works: RT, LT, RJ/LJ
	# Needs Work: Vector RJ for angles
	def design_commands_joy(self):
		info_list = []
		# Look at each of the values for variables skid_right_trigger, skid_left_trigger, skid_right_joy, skid_left_joy
		# 	and figure out the appropriate commands to send for all 6 wheels
		# Returns a list of 6 tuples with the format Example: <addr 2-7> <speed> <angle>
		#	speed being for skid, and angle being for vector
		# Be mindful of the self.states['Control_Scheme'] with 0 being skid, and 1 being vector
		
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
		if self.states['Control_Scheme'] == 0:
			# LJ and RJ are setup using the tank drive concept - # Example: <addr 2-7> <speed> <0>
			# LJ for Left Wheels (Forward/Reverse)
			for wheel_id in self.left_wheel_ids:
				data_tuple = wheel_id, self.states['skid_left_joy'], 0
				info_list.append(data_tuple)
			# RJ for Right Wheels (Forward/Reverse)
			for wheel_id in self.right_wheel_ids:
				data_tuple = wheel_id, self.states['skid_right_joy'], 0
				info_list.append(data_tuple)
			
			# LT and RT just skid steer in place - Example: <addr 2-7> <speed> <0>
			# For RT - Left wheels Forward, Right wheels Reverse
			if self.states['skid_left_joy'] == 0 and self.states['skid_right_joy'] == 0:
				info_list = []	# If LJ/RJ were already 0, then go ahead with RT commands
				for wheel_id in self.left_wheel_ids:
					if self.states['skid_right_trigger']==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Forward (255-128)
						speed = self.states['skid_right_trigger'] / 2 - 1 # Down 1 to ensure a 0 value
						if speed == 0:
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
						if speed < 0:				# Checks to ensure no negatives
							speed = 0
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					if self.states['skid_right_trigger']==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Reverse
						speed = -(self.states['skid_right_trigger'] / 2 - 1) # Down 1 to ensure a 0 value
						if speed == 0:
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
						if speed > 0:				# Checks to ensure no positives
							speed = 0
							self.states['skid_right_trigger'] = 0	# Ensures that right trigger is 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
			# For LT - Left wheels Reverse, Right wheels Forward
			if self.states['skid_left_joy'] == 0 and self.states['skid_right_joy'] == 0 and self.states['skid_right_trigger'] == 0:
				info_list = []	# If LJ/RJ and RT were already 0, then go ahead with RT commands
				for wheel_id in self.left_wheel_ids:
					if self.states['skid_left_trigger']==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Reverse (0-127)
						speed = -(self.states['skid_left_trigger'] / 2 - 1) # Down 1 to ensure a 0 value
						if speed > 0:				# Checks to ensure no positives
							speed = 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
				for wheel_id in self.right_wheel_ids:
					if self.states['skid_left_trigger']==0:
						data_tuple = wheel_id, 0, 0
						info_list.append(data_tuple)
					else:	# Forward (255-128)
						speed = self.states['skid_left_trigger'] / 2 - 1 # Down 1 to ensure a 0 value
						if speed < 0:				# Checks to ensure no negatives
							speed = 0
						data_tuple = wheel_id, speed, 0
						info_list.append(data_tuple)
			# If everything is already 0, then LT will be allowed to run, but will reset values to 0
						
		
		# Vector Steer Mode
		elif self.states['Control_Scheme'] == 1:
			# LJ for Left/Right Wheels (Forward/Reverse) - # Example: <addr 2-7> <speed> <0>
			for wheel_id in self.left_wheel_ids:
				data_tuple = wheel_id, self.states['vector_left_joy'], 0
				info_list.append(data_tuple)
			for wheel_id in self.right_wheel_ids:
				data_tuple = wheel_id, self.states['vector_left_joy'], 0
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
			info_list.append(self.states['vector_right_joy_RightLeft'])
			info_list.append("RJ - Up")
			info_list.append(self.states['vector_right_joy_Up'])
		
		return info_list
