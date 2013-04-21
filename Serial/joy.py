############ Logitech F310 Gamepad Parser - drivejoy.py ##########
# Original Author: John Zeller
# Description:  Joy parses data coming from the Logitech F310 Gamepad and
#				updates a dictionary of drive_joy_states.

### NOTE: #####################################################################
# 1) LEAVE MODE 'OFF' there is no support in parser_core.py for MODE ON       #
# 2) This parser was built using this tutorial as a reference:		      	  #
#	http://hackshark.com/?p=147#axzz2BHTVXCFz			      				  #
# 3) Naturally the gamepad sends the following values:			    		  #
# 	LJ/RJ - Down: 0-127													      #
# 	LJ/RJ - Up: 255-128													      #
# 	LJ/RJ - Left: 255-128												      #
# 	LJ/RJ - Right: 0-127												      #
# 4) States are saved as the following values:							      #
# 	LJ/RJ - Down: 0-(-127)												      #
# 	LJ/RJ - Up: 0-127													      #
# 	LJ/RJ - Left: 0-(-127)												      #
# 	LJ/RJ - Right: 0-127												      #
###############################################################################

### Buttons/Joys Represented: #################################################
# A, B, X, Y, RB, LB, LJButton, RJButton, Back, Start, Middle			      #
# RT, LT, LeftJoy, RightJoy, Left, Right, Up, Down		  				      #
###############################################################################

### States Dictionary Reference: ##############################################
#	self.drive_joy_states = { 'A':0, 'B':0, 'X':0, 'Y':0,  		   				  #
#						'Back':0, 'Start':0, 'Middle':0,		    		  #
#						'Left':0, 'Right':0, 'Up':0, 'Down':0, 		 	      #
#						'LB':0, 'RB':0, 'LT':0, 'RT':0,			   			  #
#						'LJ/Button':0, 'RJ/Button':0, 			   			  #
#						'LJ/Left':0, 'LJ/Right':0, 'LJ/Up':0, 'LJ/Down':0,	  #
#						'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0} 	  #
###############################################################################

# import sys
import threading


class DriveJoyParser(threading.Thread):
    def __init__(self, parent, bus, roverStatus):
        threading.Thread.__init__(self)

        # Pull parameters into self
        self.parent = parent
        self.bus = bus
        #roverStatus.joyMutex.acquire()
        try:
            self.drive_joy_states = roverStatus.drive_joy_states
        except:
            print "opps"
        #finally:
        #    roverStatus.joyMutex.release()

        # Creates templist for storing the 8-byte packages from gamepad
        self.templist = []

        # All button raw packet values of data coming from gamepad
        self.buttons = {'\x00': 'A', '\x01': 'B', '\x02': 'X', '\x03': 'Y',
                        '\x04': 'LB', '\x05': 'RB', '\x06': 'Back',
                        '\x07': 'Start', '\x08': 'Middle', '\t': 'LJ/Button',
                        '\n': 'RJ/Button'}
        # List of Joy Names
        self.joys = ['LT', 'RT',
                     'LJ/LeftRight', 'LJ/UpDown', 'RJ/LeftRight',
                     'RJ/UpDown']

        # Initializes templist
        for x in range(8):
            self.templist.append(0)

    def run(self):
        # Start Parser
        while 1:
            # Read 1 byte and copy state to Byte States
            for x in range(8):
                self.templist[x] = self.bus.joy_drive.read(1)

            # BUTTON is PRESSED
            if self.templist[4] == '\x01' or self.templist[4] == '\xFF':
                self.parse_pressed_button()

            # BUTTON is RELEASED
            if self.templist[4] == '\x00':
                self.parse_released_button()

            # JOYSTICK is PRESSED
            else:
                self.parse_pressed_joy()
                self.sanitize_joys()
            # print self.drive_joy_states
            # self.parent.Refresh()

    def sanitize_joys(self):
        # Adjusts the joy states when close to 0, to make sure 0 happens
        for joy in self.joys:
            value = self.drive_joy_states[joy]
            if (value <= 20) and (value > 0):
                self.drive_joy_states[joy] = 0
            elif (value >= -20) and (value < 0):
                self.drive_joy_states[joy] = 0

    def parse_pressed_button(self):
        # Updates states of buttons to 1 (on)
        if self.templist[6] == '\x01' and self.templist[5] == '\x00':  # Letters,
                                                                       # Start/Back
            self.drive_joy_states[self.buttons[self.templist[7]]] = 1
        elif self.templist[6] == '\x02' and self.templist[5] == '\x80':  # D-Pad L/U
            if self.templist[7] == '\x06':  # Left
                self.drive_joy_states['Left'] = 1
            elif self.templist[7] == '\x07':  # Up
                self.drive_joy_states['Up'] = 1
        elif self.templist[6] == '\x02' and self.templist[5] == '\x7F':  # D-Pad R/D
            if self.templist[7] == '\x06':  # Right
                self.drive_joy_states['Right'] = 1
            elif self.templist[7] == '\x07':  # Down
                self.drive_joy_states['Down'] = 1

        # print self.drive_joy_states
    def parse_pressed_joy(self):
        # Updates joy states with values 0-255 as ints
        if self.templist[7] == '\x02' and self.templist[6] == '\x02':  # LT
            if ord(self.templist[5]) >= 128:
                val = ord(self.templist[5]) - 128
                self.drive_joy_states['LT'] = val
            elif ord(self.templist[5]) <= 127:
                val = ord(self.templist[5]) + 127
                self.drive_joy_states['LT'] = val
        elif self.templist[7] == '\x05' and self.templist[6] == '\x02':  # RT
            if ord(self.templist[5]) >= 128:
                val = ord(self.templist[5]) - 128
                self.drive_joy_states['RT'] = val
            elif ord(self.templist[5]) <= 127:
                val = ord(self.templist[5]) + 127
                self.drive_joy_states['RT'] = val
        elif self.templist[7] == '\x00' and self.templist[6] == '\x02':  # L-Joy L/R
            if ord(self.templist[5]) <= 127:  # Right
                val = ord(self.templist[5])
                self.drive_joy_states['LJ/Right'] = val
                self.drive_joy_states['LJ/LeftRight'] = val
            elif ord(self.templist[5]) >= 128:  # Left
                val = ord(self.templist[5]) - 255
                self.drive_joy_states['LJ/Left'] = val
                self.drive_joy_states['LJ/LeftRight'] = val
        elif self.templist[7] == '\x01' and self.templist[6] == '\x02':  # L-Joy U/D
            if ord(self.templist[5]) <= 127:  # Down
                val = -(ord(self.templist[5]))		# Flip to negative
                self.drive_joy_states['LJ/Down'] = val
                self.drive_joy_states['LJ/UpDown'] = val
            elif ord(self.templist[5]) >= 128:  # Up
                val = (ord(self.templist[5]) - 255) * -1  # Flip to positive
                self.drive_joy_states['LJ/Up'] = val
                self.drive_joy_states['LJ/UpDown'] = val
        elif self.templist[7] == '\x03' and self.templist[6] == '\x02':  # R-Joy L/R
            if ord(self.templist[5]) <= 127:  # Right
                val = ord(self.templist[5])
                self.drive_joy_states['RJ/Right'] = val
                self.drive_joy_states['RJ/LeftRight'] = val
            elif ord(self.templist[5]) >= 128:  # Left
                val = ord(self.templist[5]) - 255
                self.drive_joy_states['RJ/Left'] = val
                self.drive_joy_states['RJ/LeftRight'] = val
        elif self.templist[7] == '\x04' and self.templist[6] == '\x02':  # R-Joy U/D
            if ord(self.templist[5]) <= 127:  # Down
                val = -(ord(self.templist[5]))		# Flip to negative
                self.drive_joy_states['RJ/Down'] = val
                self.drive_joy_states['RJ/UpDown'] = val
            elif ord(self.templist[5]) >= 128:  # Up
                val = (ord(self.templist[5]) - 255) * -1  # Flip to positive
                self.drive_joy_states['RJ/Up'] = val
                self.drive_joy_states['RJ/UpDown'] = val

        # print self.drive_joy_states

    def parse_released_button(self):
        # Updates states of buttons to 0(off)
        if self.templist[5] == '\x00' and self.templist[6] == '\x01':  # Letters,
                                                                                                                          # Start/Stop,
                                                                                                                          # L/RJ
                                                                                                                          # Button
            self.drive_joy_states[self.buttons[self.templist[7]]] = 0
        elif self.templist[5] == '\x00' and self.templist[6] == '\x02':  # D-Pad
            if self.templist[7] == '\x07':  # D-Pad, Up/Down
                if self.drive_joy_states['Up'] == 1:  # Up
                    self.drive_joy_states['Up'] = 0
                elif self.drive_joy_states['Down'] == 1:  # Down
                    self.drive_joy_states['Down'] = 0
            elif self.templist[7] == '\x06':  # D-Pad, Left/Right
                if self.drive_joy_states['Left'] == 1:  # Left
                    self.drive_joy_states['Left'] = 0
                elif self.drive_joy_states['Right'] == 1:  # Right
                    self.drive_joy_states['Right'] = 0

        # print self.drive_joy_states


class ArmJoyParser(threading.Thread):
    def __init__(self, parent, bus, roverStatus):
        threading.Thread.__init__(self)

        # Pull parameters into self
        self.parent = parent
        self.bus = bus
        #roverStatus.joyMutex.acquire()
        try:
            self.arm_joy_states = roverStatus.arm_joy_states
        except:
            print "opps"
        #finally:
        #    roverStatus.joyMutex.release()

        # Creates templist for storing the 8-byte packages from gamepad
        self.templist = []

        # All button raw packet values of data coming from gamepad
        self.buttons = {'\x00': 'A', '\x01': 'B', '\x02': 'X', '\x03': 'Y',
                        '\x04': 'LB', '\x05': 'RB', '\x06': 'Back',
                        '\x07': 'Start', '\x08': 'Middle', '\t': 'LJ/Button',
                        '\n': 'RJ/Button'}
        # List of Joy Names
        self.joys = ['LT', 'RT',
                     'LJ/LeftRight', 'LJ/UpDown', 'RJ/LeftRight',
                     'RJ/UpDown']

        # Initializes templist
        for x in range(8):
            self.templist.append(0)

    def run(self):
        # Start Parser
        while 1:
            # Read 1 byte and copy state to Byte States
            for x in range(8):
                self.templist[x] = self.bus.joy_arm.read(1)

            # BUTTON is PRESSED
            if self.templist[4] == '\x01' or self.templist[4] == '\xFF':
                self.parse_pressed_button()

            # BUTTON is RELEASED
            if self.templist[4] == '\x00':
                self.parse_released_button()

            # JOYSTICK is PRESSED
            else:
                self.parse_pressed_joy()
                self.sanitize_joys()
            # print self.arm_joy_states
            # self.parent.Refresh()

    def sanitize_joys(self):
        # Adjusts the joy states when close to 0, to make sure 0 happens
        for joy in self.joys:
            value = self.arm_joy_states[joy]
            if (value <= 20) and (value > 0):
                self.arm_joy_states[joy] = 0
            elif (value >= -20) and (value < 0):
                self.arm_joy_states[joy] = 0

    def parse_pressed_button(self):
        # Updates states of buttons to 1 (on)
        if self.templist[6] == '\x01' and self.templist[5] == '\x00':  # Letters,
                                                                       # Start/Back
            self.arm_joy_states[self.buttons[self.templist[7]]] = 1
        elif self.templist[6] == '\x02' and self.templist[5] == '\x80':  # D-Pad L/U
            if self.templist[7] == '\x06':  # Left
                self.arm_joy_states['Left'] = 1
            elif self.templist[7] == '\x07':  # Up
                self.arm_joy_states['Up'] = 1
        elif self.templist[6] == '\x02' and self.templist[5] == '\x7F':  # D-Pad R/D
            if self.templist[7] == '\x06':  # Right
                self.arm_joy_states['Right'] = 1
            elif self.templist[7] == '\x07':  # Down
                self.arm_joy_states['Down'] = 1

        # print self.arm_joy_states
    def parse_pressed_joy(self):
        # Updates joy states with values 0-255 as ints
        if self.templist[7] == '\x02' and self.templist[6] == '\x02':  # LT
            if ord(self.templist[5]) >= 128:
                val = ord(self.templist[5]) - 128
                self.arm_joy_states['LT'] = val
            elif ord(self.templist[5]) <= 127:
                val = ord(self.templist[5]) + 127
                self.arm_joy_states['LT'] = val
        elif self.templist[7] == '\x05' and self.templist[6] == '\x02':  # RT
            if ord(self.templist[5]) >= 128:
                val = ord(self.templist[5]) - 128
                self.arm_joy_states['RT'] = val
            elif ord(self.templist[5]) <= 127:
                val = ord(self.templist[5]) + 127
                self.arm_joy_states['RT'] = val
        elif self.templist[7] == '\x00' and self.templist[6] == '\x02':  # L-Joy L/R
            if ord(self.templist[5]) <= 127:  # Right
                val = ord(self.templist[5])
                self.arm_joy_states['LJ/Right'] = val
                self.arm_joy_states['LJ/LeftRight'] = val
            elif ord(self.templist[5]) >= 128:  # Left
                val = ord(self.templist[5]) - 255
                self.arm_joy_states['LJ/Left'] = val
                self.arm_joy_states['LJ/LeftRight'] = val
        elif self.templist[7] == '\x01' and self.templist[6] == '\x02':  # L-Joy U/D
            if ord(self.templist[5]) <= 127:  # Down
                val = -(ord(self.templist[5]))      # Flip to negative
                self.arm_joy_states['LJ/Down'] = val
                self.arm_joy_states['LJ/UpDown'] = val
            elif ord(self.templist[5]) >= 128:  # Up
                val = (ord(self.templist[5]) - 255) * -1  # Flip to positive
                self.arm_joy_states['LJ/Up'] = val
                self.arm_joy_states['LJ/UpDown'] = val
        elif self.templist[7] == '\x03' and self.templist[6] == '\x02':  # R-Joy L/R
            if ord(self.templist[5]) <= 127:  # Right
                val = ord(self.templist[5])
                self.arm_joy_states['RJ/Right'] = val
                self.arm_joy_states['RJ/LeftRight'] = val
            elif ord(self.templist[5]) >= 128:  # Left
                val = ord(self.templist[5]) - 255
                self.arm_joy_states['RJ/Left'] = val
                self.arm_joy_states['RJ/LeftRight'] = val
        elif self.templist[7] == '\x04' and self.templist[6] == '\x02':  # R-Joy U/D
            if ord(self.templist[5]) <= 127:  # Down
                val = -(ord(self.templist[5]))      # Flip to negative
                self.arm_joy_states['RJ/Down'] = val
                self.arm_joy_states['RJ/UpDown'] = val
            elif ord(self.templist[5]) >= 128:  # Up
                val = (ord(self.templist[5]) - 255) * -1  # Flip to positive
                self.arm_joy_states['RJ/Up'] = val
                self.arm_joy_states['RJ/UpDown'] = val

        # print self.arm_joy_states

    def parse_released_button(self):
        # Updates states of buttons to 0(off)
        if self.templist[5] == '\x00' and self.templist[6] == '\x01':  # Letters,
                                                                                                                          # Start/Stop,
                                                                                                                          # L/RJ
                                                                                                                          # Button
            self.arm_joy_states[self.buttons[self.templist[7]]] = 0
        elif self.templist[5] == '\x00' and self.templist[6] == '\x02':  # D-Pad
            if self.templist[7] == '\x07':  # D-Pad, Up/Down
                if self.arm_joy_states['Up'] == 1:  # Up
                    self.arm_joy_states['Up'] = 0
                elif self.arm_joy_states['Down'] == 1:  # Down
                    self.arm_joy_states['Down'] = 0
            elif self.templist[7] == '\x06':  # D-Pad, Left/Right
                if self.arm_joy_states['Left'] == 1:  # Left
                    self.arm_joy_states['Left'] = 0
                elif self.arm_joy_states['Right'] == 1:  # Right
                    self.arm_joy_states['Right'] = 0

        # print self.arm_joy_states