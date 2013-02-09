#############################
# File Name: rover_status.py
# Author: Cameron Bowie
# Date: 2/7/13
# Description: A class to hold the rover variables. Designed to ease rover-gui interaction
#############################

import math

class RoverStatus():
    angle = 0.0
    throttle = 100
    
    fl_angle = angle
    fr_angle = angle
    ml_angle = angle
    mr_angle = angle
    rl_angle = angle
    rr_angle = angle
    
    fl_throttle = throttle
    fr_throttle = throttle
    ml_throttle = throttle
    mr_throttle = throttle
    rl_throttle = throttle
    rr_throttle = throttle
    
    tri_hori = 0
    tri_vert = 0
    tri_zoom = 0
    
    arm_seg = [{},{},{}]
	#Arm segment lengths
    arm_seg[0]['len'] = 1.4
    arm_seg[1]['len'] = 1.3
    arm_seg[2]['len'] = 1.0
	
    wrist_angle = 0
    wrist_tilt = 0
	
    scoop_open = False
    
    voltage = 0
    
    package_one = False
    package_two = False
    package_three = False
    package_four = False
    package_five = False
    package_six = False
    
    soil_moisture = 0
    conductivity = 0
    salinity = 0
    f_temp = 0
    c_temp = 0
    
    def UpdateProbe(self):
        pass
        
    def SetAngle(self, angle):
        self.angle = math.radians(angle)

        self.fl_angle = self.angle
        self.fr_angle = self.angle
        self.ml_angle = self.angle
        self.mr_angle = self.angle
        self.rl_angle = self.angle
        self.rr_angle = self.angle
        
    def SetThrottle(self, throttle):
        self.throttle = throttle
        
        self.fl_throttle = self.throttle
        self.fr_throttle = self.throttle
        self.ml_throttle = self.throttle
        self.mr_throttle = self.throttle
        self.rl_throttle = self.throttle
        self.rr_throttle = self.throttle
