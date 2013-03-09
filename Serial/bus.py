########## Bus ##########

# Original Author: John Zeller

# Bus initializes the ports for use on the base station, and offers
# them up as easy to access attributes. Additionally, there is the
# option to reset any or all ports by using the restart function.

import serial

class Bus(object):
        def __init__(self):
            print "bus"
            self.openDrive()
            self.openArm()
            self.openRover()

        def openDrive(self):
            try:
                self.joy_drive = open('/dev/input/js1', 'r')
            except:
                print "Drive Joy is not found at /dev/input/js1"

        def openArm(self):
            try:
                self.joy_arm = open('/dev/input/js1', 'r')
            except:
                print "Arm Joy is not found at /dev/input/js1"

        def openRover(self):
            try:
                self.rover = serial.Serial('/dev/ttyUSB2',
                                           baudrate=115200)
            except:
                print "Rover is not found at /dev/ttyUSB2"

        def restart(self, bus_name):
                if bus_name == 'joy_drive':
                    self.joy_drive.close()
                    self.openDrive()
                elif bus_name=='joy_arm':
                    self.joy_arm.close()
                    self.openArm()
                elif bus_name == 'rover':
                    self.rover.close()
                    self.openRover()
                elif bus_name == 'all':
                        self.restart('joy_drive')
                        self.restart('joy_arm')
                        self.restart('rover')
