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
        self.waitTime = 0.2 # Wait 20ms between packet cycles
        # Addresses for Rover modules - Wheels are [front, middle, back]
        #                               Arm is [elbow1, elbow2, wrist]
        self.address = {'beaglebone':1, 'leftWheels':[2, 3, 4],         \
                        'rightWheels':[5, 6, 7], 'tripod': 8,           \
                        'arm':[9, 10, 11]}

    def run(self):
        while 1:
            # Make Joy Drive Commands
            for commands in self.poll_joy_drivecommand():
                self.joy_queue.put(command)
            # Make Joy Arm Commands
                # Do something
            # Make Button Commands
            #self.joy_queue.put(self.poll_button_command())
            
            sleep(self.waitTime)
            
    def poll_joy_drivecommand(self):
        # Returns list of 6 tuples of drive commands in the form
        # (addr, speed, angle)
        command_list = []
        if self.roverStatus.control_scheme == 'tank':
            # LJ controls left wheels, RJ controls right wheels
            # Left Wheels
            if self.joy_states['LJ/Up'] != 0:
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(self.joy_states['LJ/Up'])
                    command_list.append(wheelAddr, speed, 0)
            elif self.joy_states['LJ/Down'] != 0:
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(self.joy_states['LJ/Down'])
                    command_list.append(wheelAddr, speed, 0)
            else:
                for wheelAddr in self.address['leftWheels']:
                    command_list.append(wheelAddr, 0, 0)
                
            # Right Wheels
            if self.joy_states['RJ/Up'] != 0:
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(self.joy_states['RJ/Up'])
                    command_list.append(wheelAddr, speed, 0)
            elif self.joy_states['RJ/Down'] != 0:
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(self.joy_states['RJ/Down'])
                    command_list.append(wheelAddr, speed, 0)
            else:
                for wheelAddr in self.address['rightWheels']:
                    command_list.append(wheelAddr, 0, 0)
                
            # Left Trigger - Right FWD, Left Rev
            if self.joy_states['LT'] != 0:
                # Divide LT by 2 so that it's a value from 0 to 127
                velocity = self.joy_states['LT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(-(velocity))
                    command_list.append(wheelAddr, speed, 0)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(velocity)
                    command_list.append(wheelAddr, speed, 0)
            else:
                for wheelAddr in self.address['leftWheels']:
                    command_list.append(wheelAddr, 0, 0)
                for wheelAddr in self.address['rightWheels']:
                    command_list.append(wheelAddr, 0, 0)
            
            # Right Trigger - Left FWD, Right Rev
            if self.joy_states['RT'] != 0:
                # Divide RT by 2 so that it's a value from 0 to 127
                speed = self.joy_states['RT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(velocity)
                    command_list.append(wheelAddr, speed, 0)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(-(velocity))
                    command_list.append(wheelAddr, speed, 0)
            else:
                for wheelAddr in self.address['leftWheels']:
                    command_list.append(wheelAddr, 0, 0)
                for wheelAddr in self.address['rightWheels']:
                    command_list.append(wheelAddr, 0, 0)
        elif self.roverStatus.control_scheme == 'vector':
            # do vector
            nothing = 0
        elif self.roverStatus.control_scheme == 'explicit':
            # do explicit
            nothing = 0
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
                        command_list.append(wheelAddr, speed, angle)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, speed, angle)
                    else:
                        command_list.append(wheelAddr, speed, 0)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(velocity)
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, speed, angle)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, speed, angle)
                    else:
                        command_list.append(wheelAddr, speed, 0)
            else:
                for wheelAddr in self.address['leftWheels']:
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, 0, angle)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, 0, angle)
                    else:
                        command_list.append(wheelAddr, 0, 0)
                for wheelAddr in self.address['rightWheels']:
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, 0, angle)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, 0, angle)
                    else:
                        command_list.append(wheelAddr, 0, 0)
            
            # Right Trigger - Left FWD, Right Rev
            if self.joy_states['LT'] != 0:
                # Divide LT by 2 so that it's a value from 0 to 127
                velocity = self.joy_states['LT'] / 2
                for wheelAddr in self.address['leftWheels']:
                    speed = self.intToByte(velocity)
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, speed, angle)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, speed, angle)
                    else:
                        command_list.append(wheelAddr, speed, 0)
                for wheelAddr in self.address['rightWheels']:
                    speed = self.intToByte(-(velocity))
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, speed, angle)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, speed, angle)
                    else:
                        command_list.append(wheelAddr, speed, 0)
            else:
                for wheelAddr in self.address['leftWheels']:
                    if wheelAddr == 2: # Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, 0, angle)
                    elif wheelAddr == 4: #Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, 0, angle)
                    else:
                        command_list.append(wheelAddr, 0, 0)
                for wheelAddr in self.address['rightWheels']:
                    if wheelAddr == 5: # Angle: 45
                        angle = self.intToByte(angle)
                        command_list.append(wheelAddr, 0, angle)
                    elif wheelAddr == 7: #Angle: -45
                        angle = self.intToByte(-(angle))
                        command_list.append(wheelAddr, 0, angle)
                    else:
                        command_list.append(wheelAddr, 0, 0)
        
        # Emergency Stop All Systems - Middle Button
        if self.joy_states['Middle'] == 1:
            for wheelAddr in self.address['leftWheels']:
                command_list.append(wheelAddr, 0, 0)
            for wheelAddr in self.address['rightWheels']:
                command_list.append(wheelAddr, 0, 0)
                
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