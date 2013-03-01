########## Bus ##########

# Original Author: John Zeller

# Bus initializes the ports for use on the base station, and offers
# them up as easy to access attributes. Additionally, there is the
# option to reset any or all ports by using the restart function.

import serial

class Bus(object):
        def __init__(self):
            try:
                self.joy_rover = open('/dev/input/js0', 'r')
            except:
                print "Drive Joy is not found at /dev/input/js0"
            try:
                self.joy_arm = open('/dev/input/js1', 'r')
            except:
                print "Arm Joy is not found at /dev/input/js1"
            try:
                self.rover = serial.Serial('/dev/ttyUSB1',
                                           baudrate=115200)
            except:
                print "Rover is not found at /dev/ttyUSB1"

        def restart(self, bus_name):
                if bus_name == 'joy_rover':
                    self.joy_rover.close()
                    try:
                        self.joy_rover = open('/dev/input/js0', 'r')
                    except:
                        print "Drive Joy is not found at /dev/input/js0"
                elif bus_name=='joy_arm':
                    self.joy_arm.close()
                    try:
                        self.joy_arm = open('/dev/input/js1', 'r')
                    except:
                        print "Arm Joy is not found at /dev/input/js1"
                elif bus_name == 'rover':
                    self.tripod.close()
                    try:
                        self.rover = serial.Serial('/dev/ttyUSB1',
                                                   baudrate=115200)
                    except:
                        print "Rover is not found at /dev/ttyUSB1"
                elif bus_name == 'all':
                        self.restart('joy_rover')
                        self.restart('joy_arm')
                        self.restart('rover')
