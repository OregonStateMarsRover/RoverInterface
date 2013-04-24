########## Probe Math - probe_math.py ##########

# Original Author: John Zeller

# Probe Math uses the arm_joy_states values to calculate
# the expected states for the probe attachment.

import sys
import math
import time

# Setup Constants need for all the wheel math
def setup_constants(self):
    self.max = 100
    self.min = 0
    self.wait = 0
    self.increment = 5

def updateProbe(self):
    setup_constants(self)
    pressed = 1

    # Placeholders for joystick inputs
    x = self.roverStatus.arm_joy_states['X']
    rb = self.roverStatus.arm_joy_states['RB']
    lb = self.roverStatus.arm_joy_states['LB']

    probe_toggle = self.roverStatus.probe_toggle
    probe_distance = self.roverStatus.probe_distance

    # Calculate expected values
    if lb is pressed:
        if probe_distance > self.min:
            probe_distance -= self.increment
        time.sleep(self.wait)
    elif rb is pressed:
        if probe_distance < self.max:
            probe_distance += self.increment
        time.sleep(self.wait)
    elif x is pressed:
        if probe_toggle is False:
            probe_toggle = True
        time.sleep(self.wait)

    # Set tripod values
    self.roverStatus.probe_toggle = probe_toggle
    self.roverStatus.probe_distance = probe_distance