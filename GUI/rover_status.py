#############################
# File Name: rover_status.py
# Author: Cameron Bowie
# Date: 2/7/13
# Description: A class to hold the rover variables. Designed to ease rover-gui interaction
#############################

import math

class RoverStatus():
    def __init__(self, roverStatusMutex, joyMutex):
        self.roverStatusMutex = roverStatusMutex
        self.joyMutex = joyMutex

    # drive_mode = 'zeroRadius'
    # drive_mode = 'vector'
    # drive_mode = 'explicit'
    # drive_mode = 'independent'
    drive_mode = 'tank'

    # 3    0
    # 4    1
    # 5    2

    # TODO: make wheels 2 to 7 (starting with front left, ending with rear right)
    wheel = [{}, {}, {}, {}, {}, {}]

    wheel[0]['angle'] = 0
    wheel[1]['angle'] = 0
    wheel[2]['angle'] = 0
    wheel[3]['angle'] = 0
    wheel[4]['angle'] = 0
    wheel[5]['angle'] = 0

    wheel[0]['velo'] = 0
    wheel[1]['velo'] = 0
    wheel[2]['velo'] = 0
    wheel[3]['velo'] = 0
    wheel[4]['velo'] = 0
    wheel[5]['velo'] = 0

    # fl_angle = wheel[0]['angle']
    # fr_angle = wheel[3]['angle']
    # ml_angle = wheel[1]['angle']
    # mr_angle = wheel[4]['angle']
    # rl_angle = wheel[2]['angle']
    # rr_angle = wheel[5]['angle']

    # Create a dictionary to be used to keep states from joy.py
    drive_joy_states = {'A': 0, 'B': 0, 'X': 0, 'Y': 0,
                        'Back': 0, 'Start': 0, 'Middle': 0,
                        'Left': 0, 'Right': 0, 'Up': 0, 'Down': 0,
                        'LB': 0, 'RB': 0, 'LT': 0, 'RT': 0,
                        'LJ/Button': 0, 'RJ/Button': 0,
                        'LJ/UpDown': 0, 'RJ/UpDown': 0, 'LJ/LeftRight': 0,
                        'RJ/LeftRight': 0, }

    arm_joy_states = {'A': 0, 'B': 0, 'X': 0, 'Y': 0,
                      'Back': 0, 'Start': 0, 'Middle': 0,
                      'Left': 0, 'Right': 0, 'Up': 0, 'Down': 0,
                      'LB': 0, 'RB': 0, 'LT': 0, 'RT': 0,
                      'LJ/Button': 0, 'RJ/Button': 0,
                      'LJ/UpDown': 0, 'RJ/UpDown': 0, 'LJ/LeftRight': 0,
                      'RJ/LeftRight': 0, }

    angle = 0
    throttle = 100

    tri_hori = 0
    tri_vert = 0
    tri_zoom = 0

    arm_seg = [{}, {}, {}]

    # Arm segment lengths
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

        # self.fl_angle = self.angle
        # self.fr_angle = self.angle
        # self.ml_angle = self.angle
        # self.mr_angle = self.angle
        # self.rl_angle = self.angle
        # self.rr_angle = self.angle

    def SetThrottle(self, throttle):
        self.throttle = throttle

        # self.fl_throttle = self.throttle
        # self.fr_throttle = self.throttle
        # self.ml_throttle = self.throttle
        # self.mr_throttle = self.throttle
        # self.rl_throttle = self.throttle
        # self.rr_throttle = self.throttle
