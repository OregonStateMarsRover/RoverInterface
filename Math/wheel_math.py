# This code is not complete!
# This code will letter be implemented into the GUI

import math


def setup_constants(self):
    self.b = 0.381
    self.w = 0.7396 / 2
    self.R = 0.232
    self.vMax = 1.3
    self.cMax = 1.0 / self.w - 0.001
    self.thetaMax = (3.14159 / 180) * 140


def input_joystick(self):
    self.right_joystick_percent = self.hs1.value
    self.left_joystick_percent = self.hs2.value


#Ackerman (Explicit) steering mode is selected:
def explicit(self):
    input_joystick()
    #outputs (target values)
    c = (self.right_joystick_percent / 100.0) * self.cMax
    v = (self.left_joystick_percent / 100.0) * self.vMax
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

    #(rad/s) rotation rate of drive motor 1
    omega1 = v1 / self.R
    omega2 = v2 / self.R
    omega3 = omega1
    omega4 = v4 / self.R
    omega5 = v5 / self.R
    omega6 = omega4

    self.wheel2['angle'] = theta1
    self.wheel3['angle'] = theta2
    self.wheel4['angle'] = theta3
    self.wheel5['angle'] = theta4
    self.wheel6['angle'] = theta5
    self.wheel7['angle'] = theta6
    self.wheel2['velo']  = v1
    self.wheel3['velo']  = v2
    self.wheel4['velo']  = v3
    self.wheel5['velo']  = v4
    self.wheel6['velo']  = v5
    self.wheel7['velo']  = v6
    self.wheel2['omega'] = omega1
    self.wheel3['omega'] = omega2
    self.wheel4['omega'] = omega3
    self.wheel5['omega'] = omega4
    self.wheel6['omega'] = omega5
    self.wheel7['omega'] = omega6


#Vector (Crab) steering mode is selected:
def vector(self):
    input_joystick()

#(radians) steering angle of all wheels
    theta = (self.right_joystick_percent / 100.0) * self.thetaMax

#(m/s) linear velocity of all drive wheels
    v = (self.left_joystick_percent / 100.0) * self.vMax
#(radians/s) rotation rate of all drive motors
    omega = v / self.R

    self.wheel2['angle'] = theta
    self.wheel3['angle'] = theta
    self.wheel4['angle'] = theta
    self.wheel5['angle'] = theta
    self.wheel6['angle'] = theta
    self.wheel7['angle'] = theta
    self.wheel2['velo']  = v
    self.wheel3['velo']  = v
    self.wheel4['velo']  = v
    self.wheel5['velo']  = v
    self.wheel6['velo']  = v
    self.wheel7['velo']  = v
    self.wheel2['omega'] = omega
    self.wheel3['omega'] = omega
    self.wheel4['omega'] = omega
    self.wheel5['omega'] = omega
    self.wheel6['omega'] = omega
    self.wheel7['omega'] = omega


# %% Zero-Radius (In-Place) steering mode is selected:
def zeroRadius(self):
    input_joystick()

    #(radians) steering angle of wheel 1
    theta1 = math.atan(self.b / self.w)
    theta2 = 0
    theta3 = -theta1
    theta4 = -theta1
    theta5 = 0
    theta6 = theta1

#(m/s) linear velocity of drive wheel 1
    v1 = (self.left_joystick_percent / 100.0) * self.vMax * 0.5
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

    self.wheel2['angle'] = theta1
    self.wheel3['angle'] = theta2
    self.wheel4['angle'] = theta3
    self.wheel5['angle'] = theta4
    self.wheel6['angle'] = theta5
    self.wheel7['angle'] = theta6
    self.wheel2['velo']  = v1
    self.wheel3['velo']  = v2
    self.wheel4['velo']  = v3
    self.wheel5['velo']  = v4
    self.wheel6['velo']  = v5
    self.wheel7['velo']  = v6
    self.wheel2['omega'] = omega1
    self.wheel3['omega'] = omega2
    self.wheel4['omega'] = omega3
    self.wheel5['omega'] = omega4
    self.wheel6['omega'] = omega5
    self.wheel7['omega'] = omega6
