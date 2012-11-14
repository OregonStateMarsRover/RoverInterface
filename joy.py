########## XBox Controller Parser ##########

# Original Author: John Zeller

### NOTES #######################################################
# 1) LEAVE MODE 'OFF'    					#
# 2) This parser was built using this tutorial as a reference:	#
#	http://hackshark.com/?p=147#axzz2BHTVXCFz		#
#################################################################

#### Buttons/Joys Represented: ##########################
# A, B, X, Y, RB, LB, LJButton, RJButton, Back, Start	#
# RT, LT, LeftJoy, RightJoy				#
# 							#
# Buttons/Joys NOT Represented, with Mode ON:		#
#  Up, Down, Left, Right, LeftJoy			#
#########################################################

#### Possible Additions: ################################################################
# 1) When Mode is activated, NOTHING should work, just keep MODE disabled as a choice	#
# 2) When the Joy hits back to 0, then send a 0 speed command... sometimes it ends with	#
#    a speed value other than 0								#
# 3) In case of artifacts in serial communication, initialize communication with all 0	#
#    values for speeds, just in case the rover is given a GO command, when it shouldn't	#

import sys

# Open the input of /dev/input/js0 with only read permissions
pipe_joy = open('/dev/input/js0', 'r')
pipe_out = open('/dev/ttyUSB2', 'w')

# Initialize lists and dictionaries
templist = []
joy_254 = {}
joy_127 = {}
joymap_counter_254 = float(0.00)
joymap_counter_127 = float(0.00)

for x in range(8):
	templist.append(0)
buttons = {'\x00':'A', '\x01':'B', '\x02':'X', '\x03':'Y', \
		'\x04':'LB', '\x05':'RB', '\x06':'Back', '\x07':'Start', \
		'\x08':'Middle', '\t':'LJ - Button', '\n':'RJ - Button'}
for x in range(0,255):
	joy_254[x] = float(joymap_counter_254)
	joymap_counter_254 += float(0.390625)
for x in range(0,128):
	joy_127[x] = float(joymap_counter_127)
	joymap_counter_127 += 0.7874015748

# Start Parser
while 1:
	# Read 1 byte
	for x in range(8):
		templist[x] = pipe_joy.read(1)

	# BUTTON is PRESSED
	if templist[4]=='\x01' or templist[4]=='\xFF':
		# Check if D-Pad or Letters/Start/Stop
		if templist[6]=='\x01' and templist[5]=='\x00': # Letters, Start/Stop, 
								# 	or LJ/RJ Buttons 
			pipe_out.write(buttons[templist[7]])
		elif templist[6]=='\x02' and templist[5]=='\x80': # D-Pad, Left/Up
			if templist[7]=='\x06':	# Left
				pipe_out.write("Left")
			elif templist[7]=='\x07': # Up
				pipe_out.write("Up")
		elif templist[6]=='\x02' and templist[5]=='\x7F': # D-Pad, Right/Down
			if templist[7]=='\x06': # Right
				pipe_out.write("Right")
                       	elif templist[7]=='\x07': # Down
                       	        pipe_out.write("Down")
	# JOYSTICK is PRESSED
	if templist[7]=='\x02' and templist[6]=='\x02': # LT
		if ord(templist[5])>=128:
			val = "%.2f" % joy_254[ord(templist[5]) - 128]
			pipe_out.write("LT - " + val)
		if ord(templist[5])<=127:
			val = "%.2f" % joy_254[ord(templist[5]) + 127]
			pipe_out.write("LT - " + val)
		pipe_out.write("\n\r")
	elif templist[7]=='\x05' and templist[6]=='\x02': # RT
		if ord(templist[5])>=128:
			val = "%.2f" % joy_254[ord(templist[5]) - 128]
                        pipe_out.write("RT - " + val)
                if ord(templist[5])<=127:
			val = "%.2f" % joy_254[ord(templist[5]) + 127]
                        pipe_out.write("RT - " + val)
		pipe_out.write("\n\r")           
	elif templist[7]=='\x00' and templist[6]=='\x02': # Left-Joy L/R
		if ord(templist[5])<=127: # Right
			val = "%.2f" % joy_127[ord(templist[5])]
			pipe_out.write("LJ/Right - " + val)
                	pipe_out.write("\n\r")
		if ord(templist[5])>=128: # Left
			val = "%.2f" % joy_127[abs(ord(templist[5]) - 254)]
                        pipe_out.write("LJ/Left - " + val)
                        pipe_out.write("\n\r")
        elif templist[7]=='\x01' and templist[6]=='\x02': # Left-Joy U/D
		if ord(templist[5])<=127: # Down
			val = "%.2f" % joy_127[ord(templist[5])]
                        pipe_out.write("LJ/Down - " + val)
                        pipe_out.write("\n\r")
		if ord(templist[5])>=128: # Up
			val = "%.2f" % joy_127[abs(ord(templist[5]) - 254)]
                        pipe_out.write("LJ/Up - " + val)
                        pipe_out.write("\n\r")
        elif templist[7]=='\x03' and templist[6]=='\x02': # Right-Joy L/R
		if ord(templist[5])<=127: # Right
			val = "%.2f" % joy_127[ord(templist[5])]
                        pipe_out.write("RJ/Right - " + val)
                        pipe_out.write("\n\r")
		if ord(templist[5])>=128: # Left
			val = "%.2f" % joy_127[abs(ord(templist[5]) - 254)]
                        pipe_out.write("RJ/Left - " + val)
                        pipe_out.write("\n\r")
        elif templist[7]=='\x04' and templist[6]=='\x02': # Right-Joy U/D
		if ord(templist[5])<=127: # Down
			val = "%.2f" % joy_127[ord(templist[5])]
                        pipe_out.write("RJ/Down - " + val)
                        pipe_out.write("\n\r")
		if ord(templist[5])>=128: # Up
			val = "%.2f" % joy_127[abs(ord(templist[5]) - 254)]
                        pipe_out.write("RJ/Up - " + val)
                        pipe_out.write("\n\r")

	# UNIVERSALLY is RELEASED
	if templist[4]=='\x00':
                if templist[5]=='\x00': # Letters, Start/Stop, or LJ/RJ Buttons
                        pipe_out.write("\n\r")
                elif templist[5]=='\x80': # D-Pad, Left/Up
                        if templist[7]=='\x06': # Left
                                pipe_out.write("\n\r")
                        elif templist[7]=='\x07': # Up
                                pipe_out.write("\n\r")
                elif templist[5]=='\x7F': # D-Pad, Right/Down
                        if templist[7]=='\x06': # Right
                                pipe_out.write("\n\r")
                        elif templist[7]=='\x07': # Down
                                pipe_out.write("\n\r")



############ Development Tools ############

### List byte in neat line ###
#       list = []
#       for x in range(8):
#               val = repr(templist[x])
#               pipe_out.write(str(val[3:5] + "\t")
#       pipe_out.write(str(repr(templist)))
#       pipe_out.write("\n\r")

