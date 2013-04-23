import math

def updateArm(self):
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
    #self.roverStatus.wrist_tilt = 0


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
