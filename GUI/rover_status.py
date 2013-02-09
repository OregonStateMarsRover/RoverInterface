#############################
# File Name: rover_status.py
# Author: Cameron Bowie
# Date: 2/7/13
# Description: A class to hold the rover variables. Designed to ease rover-gui interaction
#############################

class RoverStatus():
    fl_angle = 0
    fr_angle = 0
    ml_angle = 0
    mr_angle = 0
    rl_angle = 0
    rr_angle = 0
    
    angle = 0
    throttle = 100
    
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
