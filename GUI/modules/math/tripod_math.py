########## Tripod Math - tripod_math.py ##########

# Original Author: John Zeller

# Tripod Math uses the arm_joy_states values to calculate
# the expected states for the tripod.

import sys
import math
import time

# Setup Constants need for all the wheel math
def setup_constants(self):
    self.center = 0
    self.max = 127
    self.min = -127
    self.wait = 0
    self.increment = 5

# from -100 to 100
def updateTripod(self):
    setup_constants(self)
    pressed = 1

    # Placeholders for joystick inputs
    up = self.roverStatus.drive_joy_states['Up']
    down = self.roverStatus.drive_joy_states['Down']
    left = self.roverStatus.drive_joy_states['Left']
    right = self.roverStatus.drive_joy_states['Right']
    y = self.roverStatus.drive_joy_states['Y']
    rb = self.roverStatus.drive_joy_states['RB']
    lb = self.roverStatus.drive_joy_states['LB']
    tri_hori = self.roverStatus.tri_hori
    tri_vert = self.roverStatus.tri_vert
    tri_zoom = self.roverStatus.tri_zoom

    # Calculate expected values
    if up is pressed:
        if tri_vert < self.max:
            tri_vert += self.increment
        time.sleep(self.wait)
    elif down is pressed:
        if tri_vert > self.min:
            tri_vert -= self.increment
        time.sleep(self.wait)
    elif right is pressed:
        if tri_hori < self.max:
            tri_hori += self.increment
        time.sleep(self.wait)
    elif left is pressed:
        if tri_hori > self.min:
            tri_hori -= self.increment
        time.sleep(self.wait)
    elif y is pressed:
        tri_hori = self.center
        tri_vert = self.center
        time.sleep(self.wait)
    elif rb is pressed:
        if tri_zoom < 100:
            tri_zoom += self.increment
        time.sleep(self.wait)
    elif lb is pressed:
        if tri_zoom > 0:
            tri_zoom -= self.increment
        time.sleep(self.wait)

    # Set tripod values
    self.roverStatus.tri_hori = tri_hori
    self.roverStatus.tri_vert = tri_vert
    self.roverStatus.tri_zoom = tri_zoom