import wx
import math

class DriveSim(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500, 320), style=wx.BORDER_SUNKEN)
        
        self.roverStatus = roverStatus
        
        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)
        
        stWheelDiagram = wx.StaticText(self, label="Wheel Diagram", pos=(170, 10))
        stWheelDiagram.SetFont(titleFont)
        
        self.fl_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.fl_angle, size=(60, -1), pos=(100, 67))
        self.fl_angleSpin.SetRange(-90, 90)
        self.fr_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.fr_angle, size=(60, -1), pos=(340, 67))
        self.fr_angleSpin.SetRange(-90, 90)
        self.ml_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.ml_angle, size=(60, -1), pos=(100, 157))
        self.ml_angleSpin.SetRange(-90, 90)
        self.mr_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.mr_angle, size=(60, -1), pos=(340, 157))
        self.mr_angleSpin.SetRange(-90, 90)
        self.rl_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.rl_angle, size=(60, -1), pos=(100, 247))
        self.rl_angleSpin.SetRange(-90, 90)
        self.rr_angleSpin = wx.SpinCtrl(self, value='%d' % self.roverStatus.rr_angle, size=(60, -1), pos=(340, 247))
        self.rr_angleSpin.SetRange(-90, 90)
        
    def OnPaint(self, e):
        self.fl_angleSpin.SetValue(-math.degrees(self.roverStatus.fl_angle))
        self.fr_angleSpin.SetValue(-math.degrees(self.roverStatus.fr_angle))
        self.ml_angleSpin.SetValue(-math.degrees(self.roverStatus.ml_angle))
        self.mr_angleSpin.SetValue(-math.degrees(self.roverStatus.mr_angle))
        self.rl_angleSpin.SetValue(-math.degrees(self.roverStatus.rl_angle))
        self.rr_angleSpin.SetValue(-math.degrees(self.roverStatus.rr_angle))
        
        front_left = self.draw_wheel(self.roverStatus.fl_angle, (200, 80), self.roverStatus.fl_throttle)
        front_right = self.draw_wheel(self.roverStatus.fr_angle, (300, 80), self.roverStatus.fr_throttle)
        middle_left = self.draw_wheel(self.roverStatus.ml_angle, (200, 170), self.roverStatus.ml_throttle)
        middle_right = self.draw_wheel(self.roverStatus.mr_angle, (300, 170), self.roverStatus.mr_throttle)
        rear_left = self.draw_wheel(self.roverStatus.rl_angle, (200, 260), self.roverStatus.rl_throttle)
        rear_right = self.draw_wheel(self.roverStatus.rr_angle, (300, 260), self.roverStatus.rr_throttle)
        
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
        
    def set_angle(self, angle, wheelChange=[0]):
        for wheel in wheelChange:
            if wheel == 0 or wheel == 1:
                self.roverStatus.fl_angle = math.radians(-angle)
            if wheel == 0 or wheel == 2:
                self.roverStatus.fr_angle = math.radians(-angle)
            if wheel == 0 or wheel == 3:
                self.roverStatus.ml_angle = math.radians(-angle)
            if wheel == 0 or wheel == 4:
                self.roverStatus.mr_angle = math.radians(-angle)
            if wheel == 0 or wheel == 5:
                self.roverStatus.rl_angle = math.radians(-angle)
            if wheel == 0 or wheel == 6:
                self.roverStatus.rr_angle = math.radians(-angle)
            
        self.Refresh()
        
    def draw_wheel(self, angle, center_pos, throttle):
        upper_right = (int(center_pos[0] - 25 * math.sin(angle) + 12.5 * math.cos(angle)),
                       int(center_pos[1] - 25 * math.cos(angle) - 12.5 * math.sin(angle)))
        middle_right = (upper_right[0] + 25 * math.sin(angle),
                       upper_right[1] + 25 * math.cos(angle))
        lower_right = (middle_right[0] + 25 * math.sin(angle),
                       middle_right[1] + 25 * math.cos(angle))
        lower_left = (lower_right[0] - 25 * math.cos(angle),
                      lower_right[1] + 25 * math.sin(angle))
        middle_left = (lower_left[0] - 25 * math.sin(angle),
                      lower_left[1] - 25 * math.cos(angle))
        upper_left = (middle_left[0] - 25 * math.sin(angle),
                      middle_left[1] - 25 * math.cos(angle))
        
        self.dc = wx.PaintDC(self)
        self.dc.SetBrush(wx.Brush('#000000'))
        
        self.dc.DrawPolygon([upper_right, lower_right, lower_left, upper_left])
        
        if throttle >= 0:
            pos1 = (middle_right[0] - throttle//4 * math.sin(angle),
                    middle_right[1] - throttle//4 * math.cos(angle))
            pos2 = (middle_left[0] - throttle//4 * math.sin(angle),
                    middle_left[1] - throttle//4 * math.cos(angle))
            self.dc.SetBrush(wx.Brush('#00ff00'))
        else:
            pos1 = (middle_right[0] - throttle//4 * math.sin(angle),
                    middle_right[1] - throttle//4 * math.cos(angle))
            pos2 = (middle_left[0] - throttle//4 * math.sin(angle),
                    middle_left[1] - throttle//4 * math.cos(angle))
            self.dc.SetBrush(wx.Brush('#ff0000'))
        
        self.dc.DrawPolygon([pos1, middle_right, middle_left, pos2])

