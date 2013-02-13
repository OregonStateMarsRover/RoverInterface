########## Queuer - queuer.py ##########

# Original Author: John Zeller

# The Queuer looks at Rover_Status to determine, based on the values of the
# Joy, what address, speed and angle commands are necessary. It then adds
# these commands in the form of a tuple (addr, speed, angle) to the joy_queue

import sys
import time
import math
import Queue
import threading
from roverpacket import *
from bus import *
from joy import *

class Queuer(threading.Thread):
    def __init__(self, joy_queue, roverStatus):
        threading.Thread.__init__(self)
        self.joy_queue = joy_queue
        self.roverStatus = roverStatus
        self.joy_states = roverStatus.joy_states
        self.waitTime = 1 # Wait 20ms between packet cycles
        # Addresses for Rover modules - Wheels are [front, middle, back]
        #                               Arm is [elbow1, elbow2, wrist]
        self.address = {'beaglebone':1, 'leftWheels':[2, 3, 4],         \
                        'rightWheels':[5, 6, 7], 'tripod': 8,           \
                        'arm':[9, 10, 11]}

    def run(self):
        while 1:
            # Make Joy Drive Commands
            joy_command = self.poll_joy_drivecommand()
            for command in joy_command:
                self.joy_queue.put(command)
            # Make Joy Arm Commands
                # Do something
            # Make Button Commands
            #self.joy_queue.put(self.poll_button_command())
            time.sleep(self.waitTime)
            
    def poll_joy_drivecommand(self):
        # Returns list of 6 tuples of drive commands in the form
        # (addr, speed, angle)
        # Priority List (Right of Way):
		# 	1) LJ/RJ (Both because they don't have overcrossing commands)
		# 	2) RT - ONLY ALLOW if LJ/RJ are 0
		# 	3) LT - ONLY ALLOW if LJ/RJ and RT are 0
        command_list = []
        if self.roverStatus.control_scheme == 'tank':
            # LJ controls left wheels, RJ controls right wheels
            if (self.joy_states['RJ/UpDown'] or self.joy_states['LJ/UpDown']) != 0:
                # Left Wheels - LJ
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(self.joy_states['LJ/UpDown'])
                    data = wheelAddr, speed, 0
                    command_list.append(data)
                
                # Right Wheels - RJ
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(self.joy_states['RJ/UpDown'])
                    data = wheelAddr, speed, 0
                    command_list.append(data)
            
            # Right Trigger - Left FWD, Right Rev
            elif (self.joy_states['RT'] != 0) and \
                    ((self.joy_states['RJ/UpDown'] and self.joy_states['LJ/UpDown']) == 0):
                # Divide RT by 2 so that it's a value from 0 to 127
                speed = self.joy_states['RT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(velocity)
                    data = wheelAddr, speed, 0
                    command_list.append(data)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(-(velocity))
                    data = wheelAddr, speed, 0
                    command_list.append(data)
                    
            # Left Trigger - Right FWD, Left Rev
            elif (self.joy_states['LT'] != 0) and (self.joy_states['RT'] and \
                    (self.joy_states['RJ/UpDown'] and self.joy_states['LJ/UpDown']) == 0):
                # Divide LT by 2 so that it's a value from 0 to 127
                velocity = self.joy_states['LT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(-(velocity))
                    data = wheelAddr, speed, 0
                    command_list.append(data)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(velocity)
                    data = wheelAddr, speed, 0
                    command_list.append(data)
            else:
                for wheelAddr in self.address['leftWheels']:
                    data = wheelAddr, 0, 0
                    command_list.append(data)
                for wheelAddr in self.address['rightWheels']:
                    data = wheelAddr, 0, 0
                    command_list.append(data)
                    
        elif self.roverStatus.control_scheme == 'vector':
            # do vector
            nothing = 0
        elif self.roverStatus.control_scheme == 'explicit':
            # do explicit
            nothing = 0
            
        # Priority List (Right of Way):
		# 	2) RT - If RT != 0
		# 	3) LT - ONLY ALLOW if RT is 0 and LT != 0
        elif self.roverStatus.control_scheme == 'zeroRadius':
            # Adjust corner wheels to 45-degrees
            angle = 45
            # Left Trigger - Right FWD, Left Rev
            if self.joy_states['LT'] != 0:
                # Divide LT by 2 so that it's a value from 0 to 127
                velocity = self.joy_states['LT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(-(velocity))
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, speed, 0
                        command_list.append(data)
            elif (self.joy_states['LT'] == 0) and (self.joy_states['RT'] != 0):
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(velocity)
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, speed, 0
                        command_list.append(data)
            else:
                for wheelAddr in self.address['leftWheels']:
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, 0, 0
                        command_list.append(data)
                for wheelAddr in self.address['rightWheels']:
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, 0, 0
                        command_list.append(data)
            
            # Right Trigger - Left FWD, Right Rev
            if self.joy_states['LT'] != 0:
                # Divide LT by 2 so that it's a value from 0 to 127
                velocity = self.joy_states['LT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(velocity)
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, speed, 0
                        command_list.append(data)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(-(velocity))
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, speed, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, speed, 0
                        command_list.append(data)
            else:
                for wheelAddr in self.address['leftWheels']:
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, 0, 0
                        command_list.append(data)
                for wheelAddr in self.address['rightWheels']:
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        data = wheelAddr, 0, angle
                        command_list.append(data)
                    else:
                        data = wheelAddr, 0, 0
                        command_list.append(data)
        
        # Emergency Stop All Systems - Middle Button
        if self.joy_states['Middle'] == 1:
            for wheelAddr in self.address['leftWheels']:
                data = wheelAddr, 0, 0
                command_list.append(data)
            for wheelAddr in self.address['rightWheels']:
                data = wheelAddr, 0, 0
                command_list.append(data)
                
        return command_list
    
    def poll_joy_armcommand(self):
        # Returns list of 3 tuples of arm commands in the form
        # (addr, speed, angle)
        nothing = 0

    def poll_button_command(self):
        # Returns 1 tuple for a button command in the form (addr, data)
        # 
        command = None
        # Tripod Controls - (addr, vert_angle, horz_angle) - Angles -100 to 100
        # Angles should be persistent, meaning that this should change the
        # tripod angle state in roverStatus, and then that status should be
        # used to update the tripod command, if it needs updating
        
        return command
        
    def intToByte(self, int_var):
        # Description: Takes in an integer representation (-127 to 127) of
        #              speed and returns the byte representation that the
        #              bogie controllers use.
        #              (Reverse: 0-127) (Positive: 255-128)
        # NOTE: Does not work for RT or LT
        
        byte_var = 0
        if (int_var <= 0) and (int_var >= -127):
            byte_var = abs(int_var) # Converts 0 to -127 -> 0 to 127
        elif (int_var >= 0) and (int_var <= 127):
            byte_var = -(int_var) + 255 # Converts 0 to 127 -> 255 to 128
        
        return byte_var
        
    def byteToInt(self, byte_var):
        # Description: Takes in a byte representation (Reverse: 0-127)
        #              (Positive: 255-128) of speed and returns the integer
        #              representation (-127 to 127)
        
        int_var = 0
        if (byte_var >= 0) and (byte_var <= 127):
            int_var = -(byte_var) # Converts 0 to 127 -> 0 to -127
        elif (byte_var <= 255) and (byte_var >= 128):
            int_var = abs(byte_var - 255) # Converts 255 to 128 -> 0 to 127
        
        return int_var