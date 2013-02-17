#################################################################
# Filename: Wheel_math.py                                       #
# Author: Francis Vo                                            #
# Description: This file does Wheel for driving the Mars Rover. #
#################################################################

import sys
import math


# Setup Constants need for all the wheel math
def setup_constants(self):
    self.b = 0.381
    self.w = 0.7396 / 2
    self.R = 0.232
    self.vMax = 1.3
    self.cMax = 1.0 / self.w - 0.001
    self.thetaMax = (3.14159 / 180) * 140

# TODO: Math use joy status
# independent mode is selected:


def independent(self):
    # Note: no joystick input
    setup_constants(self)
    # Velocity
    v = self.roverStatus.throttle / 100.0 * self.vMax
    # Omega is the turning rate of the wheels
    omega = v / self.R

    # No setting for Wheel angle, because they all add different and independent

    # All wheels are at the same speed
    self.roverStatus.wheel[0]['velo'] = v
    self.roverStatus.wheel[1]['velo'] = v
    self.roverStatus.wheel[2]['velo'] = v
    self.roverStatus.wheel[3]['velo'] = v
    self.roverStatus.wheel[4]['velo'] = v
    self.roverStatus.wheel[5]['velo'] = v

    # Set the turning rates of each wheel
    self.roverStatus.wheel[0]['omega'] = omega
    self.roverStatus.wheel[1]['omega'] = omega
    self.roverStatus.wheel[2]['omega'] = omega
    self.roverStatus.wheel[3]['omega'] = omega
    self.roverStatus.wheel[4]['omega'] = omega
    self.roverStatus.wheel[5]['omega'] = omega


# Tank mode is selected:
def tank(self):
    setup_constants(self)
    # Placeholders for joystick inputs
    left_joystick_percent = self.roverStatus.joy_states['LJ/UpDown'] / 128.0
    right_joystick_percent = self.roverStatus.joy_states['RJ/UpDown'] / 128.0

    # max allowed speed
    v = self.roverStatus.throttle / 100.0 * self.vMax
    v_left = v * left_joystick_percent
    v_right = v * right_joystick_percent

    # all wheels are all angle 0
    self.roverStatus.wheel[0]['angle'] = 0
    self.roverStatus.wheel[1]['angle'] = 0
    self.roverStatus.wheel[2]['angle'] = 0
    self.roverStatus.wheel[3]['angle'] = 0
    self.roverStatus.wheel[4]['angle'] = 0
    self.roverStatus.wheel[5]['angle'] = 0

    # right side velocity
    self.roverStatus.wheel[0]['velo'] = v_right
    self.roverStatus.wheel[1]['velo'] = v_right
    self.roverStatus.wheel[2]['velo'] = v_right

    # left side velocity
    self.roverStatus.wheel[3]['velo'] = v_left
    self.roverStatus.wheel[4]['velo'] = v_left
    self.roverStatus.wheel[5]['velo'] = v_left

    # Do not let Wheel turn so turn rate is 0
    self.roverStatus.wheel[0]['omega'] = 0
    self.roverStatus.wheel[1]['omega'] = 0
    self.roverStatus.wheel[2]['omega'] = 0
    self.roverStatus.wheel[3]['omega'] = 0
    self.roverStatus.wheel[4]['omega'] = 0
    self.roverStatus.wheel[5]['omega'] = 0


# Ackerman (Explicit) steering mode is selected:
def explicit(self):
    setup_constants(self)
    c = (self.roverStatus.angle / 4) * self.cMax
    v = self.roverStatus.throttle / 100.0 * self.vMax

    if c == 0:
        r = 999
    else:
        r = 1.0 / c

    #(radians) steering angle of wheel 1
    theta1 = math.atan(self.b / (r + self.w))
    theta2 = 0
    theta3 = -theta1
    theta4 = math.atan(self.b / (r - self.w))
    theta5 = 0
    theta6 = -theta4

    #(m/s) linear velocity of drive motor 1
    v2 = v * (r + self.w) / r
    v5 = v * (r - self.w) / r
    v1 = v2 / math.cos(theta3)
    v3 = v1
    v4 = v5 / math.cos(theta4)
    v6 = v4

    v_max = max(math.fabs(v1), math.fabs(v2), math.fabs(v3), math.fabs(v4), math.fabs(v5), math.fabs(v6))
    v_ratio = sys.maxint if v == 0 else math.fabs(v_max / v)
    v1 = v1 / v_ratio
    v2 = v2 / v_ratio
    v3 = v3 / v_ratio
    v4 = v4 / v_ratio
    v5 = v5 / v_ratio
    v6 = v6 / v_ratio

    #(rad/s) rotation rate of drive motor 1
    omega1 = v1 / self.R
    omega2 = v2 / self.R
    omega3 = omega1
    omega4 = v4 / self.R
    omega5 = v5 / self.R
    omega6 = omega4

    self.roverStatus.wheel[0]['angle'] = theta1
    self.roverStatus.wheel[1]['angle'] = theta2
    self.roverStatus.wheel[2]['angle'] = theta3
    self.roverStatus.wheel[3]['angle'] = theta4
    self.roverStatus.wheel[4]['angle'] = theta5
    self.roverStatus.wheel[5]['angle'] = theta6
    self.roverStatus.wheel[0]['velo'] = v1
    self.roverStatus.wheel[1]['velo'] = v2
    self.roverStatus.wheel[2]['velo'] = v3
    self.roverStatus.wheel[3]['velo'] = v4
    self.roverStatus.wheel[4]['velo'] = v5
    self.roverStatus.wheel[5]['velo'] = v6
    self.roverStatus.wheel[0]['omega'] = omega1
    self.roverStatus.wheel[1]['omega'] = omega2
    self.roverStatus.wheel[2]['omega'] = omega3
    self.roverStatus.wheel[3]['omega'] = omega4
    self.roverStatus.wheel[4]['omega'] = omega5
    self.roverStatus.wheel[5]['omega'] = omega6


# Vector (Crab) steering mode is selected:
def vector(self):
    setup_constants(self)

    #(radians) steering angle of all wheels
    # theta = (self.right_joystick_percent / 100.0) * self.thetaMax
    o = self.roverStatus.joy_states['RJ/UpDown']
    a = self.roverStatus.joy_states['RJ/LeftRight']
    theta = math.atan2(o * 1.0, a * 1.0) - math.pi / 2
    v = self.roverStatus.throttle / 100.0 * self.vMax
    v = (o ** 2 + a ** 2) ** 0.5 / 129 * v
    if math.degrees(theta) < -90:
        theta += math.pi
        v = -v
    # print(math.degrees(theta))
    # theta = self.roverStatus.angle  # * self.thetaMax
    #(m/s) linear velocity of all drive wheels
    # v = (self.left_joystick_percent / 100.0) * self.vMax
    #(radians/s) rotation rate of all drive motors
    omega = v / self.R

    self.roverStatus.wheel[0]['angle'] = theta
    self.roverStatus.wheel[1]['angle'] = theta
    self.roverStatus.wheel[2]['angle'] = theta
    self.roverStatus.wheel[3]['angle'] = theta
    self.roverStatus.wheel[4]['angle'] = theta
    self.roverStatus.wheel[5]['angle'] = theta
    self.roverStatus.wheel[0]['velo'] = v
    self.roverStatus.wheel[1]['velo'] = v
    self.roverStatus.wheel[2]['velo'] = v
    self.roverStatus.wheel[3]['velo'] = v
    self.roverStatus.wheel[4]['velo'] = v
    self.roverStatus.wheel[5]['velo'] = v
    self.roverStatus.wheel[0]['omega'] = omega
    self.roverStatus.wheel[1]['omega'] = omega
    self.roverStatus.wheel[2]['omega'] = omega
    self.roverStatus.wheel[3]['omega'] = omega
    self.roverStatus.wheel[4]['omega'] = omega
    self.roverStatus.wheel[5]['omega'] = omega


# %% Zero-Radius (In-Place) steering mode is selected:
def zeroRadius(self):
    setup_constants(self)
    # input_joystick()

    #(radians) steering angle of wheel 1
    theta1 = math.atan(self.b / self.w)
    theta2 = 0
    theta3 = -theta1
    theta4 = -theta1
    theta5 = 0
    theta6 = theta1

    #(m/s) linear velocity of drive wheel 1
    right_joystick_percent = self.roverStatus.joy_states['RJ/UpDown'] / 128.0
    v1 = right_joystick_percent * self.roverStatus.throttle / 100.0 * self.vMax  # * 0.5
    v2 = v1 * (self.w / (self.b ** 2 + self.w ** 2) ** 0.5)
    v3 = v1
    v4 = -v1
    v5 = -v2
    v6 = -v1

    #(radians/s) rotation rate of drive motor 1
    omega1 = v1 / self.R
    omega2 = v2 / self.R
    omega3 = v3 / self.R
    omega4 = v4 / self.R
    omega5 = v5 / self.R
    omega6 = v6 / self.R

    self.roverStatus.wheel[0]['angle'] = theta1
    self.roverStatus.wheel[1]['angle'] = theta2
    self.roverStatus.wheel[2]['angle'] = theta3
    self.roverStatus.wheel[3]['angle'] = theta4
    self.roverStatus.wheel[4]['angle'] = theta5
    self.roverStatus.wheel[5]['angle'] = theta6
    self.roverStatus.wheel[0]['velo'] = v1
    self.roverStatus.wheel[1]['velo'] = v2
    self.roverStatus.wheel[2]['velo'] = v3
    self.roverStatus.wheel[3]['velo'] = v4
    self.roverStatus.wheel[4]['velo'] = v5
    self.roverStatus.wheel[5]['velo'] = v6
    self.roverStatus.wheel[0]['omega'] = omega1
    self.roverStatus.wheel[1]['omega'] = omega2
    self.roverStatus.wheel[2]['omega'] = omega3
    self.roverStatus.wheel[3]['omega'] = omega4
    self.roverStatus.wheel[4]['omega'] = omega5
    self.roverStatus.wheel[5]['omega'] = omega6
