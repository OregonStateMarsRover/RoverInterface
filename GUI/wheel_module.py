import wx
import math
from wheel_math import *


class DriveSim(wx.Panel):

    def __init__(self, parent, roverStatus):
        setup_constants(self)
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500, 320), style=wx.BORDER_SUNKEN)

        self.parent = parent

        self.roverStatus = roverStatus

        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)

        stWheelDiagram = wx.StaticText(self, label="Wheel Diagram", pos=(170, 10))
        stWheelDiagram.SetFont(titleFont)

        self.fl_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.wheel[3]['angle'], size=(60, -1), pos=(100, 67))
        self.fl_angleSpin.SetRange(-90, 90)
        self.fr_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.wheel[0]['angle'], size=(60, -1), pos=(340, 67))
        self.fr_angleSpin.SetRange(-90, 90)
        self.ml_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.wheel[4]['angle'], size=(60, -1), pos=(100, 157))
        self.ml_angleSpin.SetRange(-90, 90)
        self.mr_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.wheel[2]['angle'], size=(60, -1), pos=(340, 157))
        self.mr_angleSpin.SetRange(-90, 90)
        self.rl_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.wheel[5]['angle'], size=(60, -1), pos=(100, 247))
        self.rl_angleSpin.SetRange(-90, 90)
        self.rr_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.wheel[2]['angle'], size=(60, -1), pos=(340, 247))
        self.rr_angleSpin.SetRange(-90, 90)

    def OnPaint(self, e):
        if self.roverStatus.drive_mode == 'zeroRadius':
            zeroRadius(self)
        elif self.roverStatus.drive_mode == 'vector':
            vector(self)
        elif self.roverStatus.drive_mode == 'explicit':
            explicit(self)
        elif self.roverStatus.drive_mode == 'independent':
            independent(self)
        elif self.roverStatus.drive_mode == 'tank':
            tank(self)

        self.fl_angleSpin.SetValue(math.degrees(self.roverStatus.wheel[3]['angle']))
        self.fr_angleSpin.SetValue(math.degrees(self.roverStatus.wheel[0]['angle']))
        self.ml_angleSpin.SetValue(math.degrees(self.roverStatus.wheel[4]['angle']))
        self.mr_angleSpin.SetValue(math.degrees(self.roverStatus.wheel[1]['angle']))
        self.rl_angleSpin.SetValue(math.degrees(self.roverStatus.wheel[5]['angle']))
        self.rr_angleSpin.SetValue(math.degrees(self.roverStatus.wheel[2]['angle']))
        #print(self.roverStatus.fl_angle)
        front_left   = self.draw_wheel(self.roverStatus.wheel[3], (200, 80))
        front_right  = self.draw_wheel(self.roverStatus.wheel[0], (300, 80))
        middle_left  = self.draw_wheel(self.roverStatus.wheel[4], (200, 170))
        middle_right = self.draw_wheel(self.roverStatus.wheel[1], (300, 170))
        rear_left    = self.draw_wheel(self.roverStatus.wheel[5], (200, 260))
        rear_right   = self.draw_wheel(self.roverStatus.wheel[2], (300, 260))

    def OnSpinCtrl(self, e):
        obj = e.GetEventObject()
        angle = obj.GetValue()

        if obj == self.fl_angleSpin:
            self.set_angle(angle, [1])
        elif obj == self.fr_angleSpin:
            self.set_angle(angle, [2])
        elif obj == self.ml_angleSpin:
            self.set_angle(angle, [3])
        elif obj == self.mr_angleSpin:
            self.set_angle(angle, [4])
        elif obj == self.rl_angleSpin:
            self.set_angle(angle, [5])
        elif obj == self.rr_angleSpin:
            self.set_angle(angle, [6])
        self.Refresh()

    def set_angle(self, angle, wheelChange=[0]):
        for wheel in wheelChange:
            if wheel == 0 or wheel == 1:
                self.roverStatus.wheel[3]['angle'] = math.radians(angle)
            if wheel == 0 or wheel == 2:
                self.roverStatus.wheel[0]['angle'] = math.radians(angle)
            if wheel == 0 or wheel == 3:
                self.roverStatus.wheel[4]['angle'] = math.radians(angle)
            if wheel == 0 or wheel == 4:
                self.roverStatus.wheel[1]['angle'] = math.radians(angle)
            if wheel == 0 or wheel == 5:
                self.roverStatus.wheel[5]['angle'] = math.radians(angle)
            if wheel == 0 or wheel == 6:
                self.roverStatus.wheel[2]['angle'] = math.radians(angle)

        self.Refresh()


    def draw_wheel(self, wheel, pos):
        pos1 = (int(pos[0] - 25 * math.sin(wheel['angle']) + 12.5 * math.cos(wheel['angle'])),
                int(pos[1] - 25 * math.cos(wheel['angle']) - 12.5 * math.sin(wheel['angle'])))
        pos2 = (pos1[0] + 50 * math.sin(wheel['angle']), pos1[1] + 50 * math.cos(wheel['angle']))
        pos3 = (pos2[0] - 25 * math.cos(wheel['angle']), pos2[1] + 25 * math.sin(wheel['angle']))
        pos4 = (pos3[0] - 50 * math.sin(wheel['angle']), pos3[1] - 50 * math.cos(wheel['angle']))

        self.dc = wx.PaintDC(self)
        self.dc.SetBrush(wx.Brush('#000000'))

        self.dc.DrawPolygon([pos1, pos2, pos3, pos4])
        print (wheel['velo'] / self.vMax * 50 + 50)

        pos5 = (pos2[0] - 50 / 2 * math.sin(wheel['angle']), 
                pos2[1] - 50 / 2 * math.cos(wheel['angle']))
        pos6 = (pos3[0] - 50 / 2 * math.sin(wheel['angle']), 
                pos3[1] - 50 / 2 * math.cos(wheel['angle']))

        pos7 = (pos2[0] - (wheel['velo'] / self.vMax * 50 + 50) / 2 * math.sin(wheel['angle']), 
                pos2[1] - (wheel['velo'] / self.vMax * 50 + 50) / 2 * math.cos(wheel['angle']))
        pos8 = (pos3[0] - (wheel['velo'] / self.vMax * 50 + 50) / 2 * math.sin(wheel['angle']), 
                pos3[1] - (wheel['velo'] / self.vMax * 50 + 50) / 2 * math.cos(wheel['angle']))

        self.dc.SetBrush(wx.Brush('#00ff00'))

        self.dc.DrawPolygon([pos6,pos5,pos7,pos8])

        
