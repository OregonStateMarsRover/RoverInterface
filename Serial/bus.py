########## Bus ##########

# Original Author: John Zeller

# Bus initializes the ports for use on the base station, and offers
# them up as easy to access attributes. Additionally, there is the
# option to reset any or all ports by using the restart function.

import serial
#import time


class Bus(object):
        def __init__(self):
                self.joy_rover = open('/dev/input/js1', 'r')
# Disabled                self.joy_arm = open(port='/dev/input/js1', 'r')
# Disabled                self.rover = serial.Serial(port='/dev/ttyUSB2',
#                                        baudrate=115200)
                # Perhaps auto detect which is from rover?

        def restart(self, bus_name):
                if bus_name == 'joy_rover':
                        self.joy_rover.close()
                        self.joy_rover = open('/dev/input/js1', 'r')
# Disabled                elif bus_name=='joy_arm':
#                        self.joy_arm.close()
#                        self.joy_arm = open('/dev/input/js0', 'r')
                elif bus_name == 'rover':
                        self.tripod.close()
                        self.tripod = serial.Serial(port='/dev/ttyUSB1',
                                                    baudrate=115200)
                elif bus_name == 'all':
                        self.restart('joy_rover')
# Disabled                        self.restart('joy_arm')
                        self.restart('rover')
