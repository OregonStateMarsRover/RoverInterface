import math
import time

def updateArm(self):
    pressed = 1

    target = [self.roverStatus.arm_seg[1]['pos'][0], self.roverStatus.arm_seg[1]['pos'][1]]

    target[1] += .001 * self.roverStatus.arm_joy_states['LJ/UpDown']
    target[0] += .001 * self.roverStatus.arm_joy_states['LJ/LeftRight']

    for x in xrange(1, 10):
        reach(self.roverStatus, target)
    self.roverStatus.arm_seg[2]['angle'] += .0005 * self.roverStatus.arm_joy_states['RJ/UpDown']

    # Update roverStatus values used in queuer
    self.roverStatus.arm_shoulder = round(math.degrees(self.roverStatus.arm_seg[0]['angle']))
    self.roverStatus.arm_elbow = round(math.degrees(self.roverStatus.arm_seg[1]['angle']))
    self.roverStatus.wrist_angle = round(math.degrees(self.roverStatus.arm_seg[2]['angle']))
    
    # Placeholders for joystick inputs
    a = self.roverStatus.arm_joy_states['A']
    b = self.roverStatus.arm_joy_states['B']
    left = self.roverStatus.arm_joy_states['Left']
    right = self.roverStatus.arm_joy_states['Right']
    scoop_toggle = self.roverStatus.scoop_toggle
    voltage_toggle = self.roverStatus.voltage_toggle
    wrist_tilt = self.roverStatus.wrist_tilt

    # Calculate expected values
    if a is pressed:
        if scoop_toggle is True:
            scoop_toggle = False
        elif scoop_toggle is False:
            scoop_toggle = True
    elif b is pressed:
        if voltage_toggle is False:
            voltage_toggle = True
    elif right is pressed:
        if wrist_tilt < 90:
            wrist_tilt += 5
        time.sleep(self.wait)
    elif left is pressed:
        if wrist_tilt > -90:
            wrist_tilt -= 5
        time.sleep(self.wait)

    # Set scoop, voltage and wrist tilt values
    self.roverStatus.scoop_toggle = scoop_toggle
    self.roverStatus.voltage_toggle = voltage_toggle
    self.roverStatus.wrist_tilt = wrist_tilt


def reach(roverStatus, target):
    angle2 = roverStatus.arm_seg[0]['angle'] + roverStatus.arm_seg[1]['angle'] - math.pi
    angle3 = angle2 + roverStatus.arm_seg[2]['angle'] - math.pi

    dx = target[0] - roverStatus.arm_seg[0]['pos'][0]
    dy = target[1] - roverStatus.arm_seg[0]['pos'][1]
    da = math.atan2(dy, dx) - angle2
    angle2 += da / 2

    roverStatus.arm_seg[1]['angle'] = angle2 - roverStatus.arm_seg[0]['angle'] + math.pi

    dx = target[0] - math.cos(angle2) * roverStatus.arm_seg[1]['len']
    dy = target[1] - math.sin(angle2) * roverStatus.arm_seg[1]['len']
    da = math.atan2(dy, dx) - roverStatus.arm_seg[0]['angle']
    roverStatus.arm_seg[0]['angle'] += da
    math.degrees(roverStatus.arm_seg[0]['angle'])

    roverStatus.arm_seg[2]['angle'] = angle3 - angle2 + math.pi
