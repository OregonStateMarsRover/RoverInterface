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
        print(self.roverStatus.fl_angle)
        front_left = self.draw_wheel(self.roverStatus.fl_angle, (200, 80))
        front_right = self.draw_wheel(self.roverStatus.fr_angle, (300, 80))
        middle_left = self.draw_wheel(self.roverStatus.ml_angle, (200, 170))
        middle_right = self.draw_wheel(self.roverStatus.mr_angle, (300, 170))
        rear_left = self.draw_wheel(self.roverStatus.rl_angle, (200, 260))
        rear_right = self.draw_wheel(self.roverStatus.rr_angle, (300, 260))
        
        
        
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
        
    def draw_wheel(self, angle, pos):
        pos1 = (int(pos[0] - 25 * math.sin(angle) + 12.5 * math.cos(angle)), int(pos[1] - 25 * math.cos(angle) - 12.5 * math.sin(angle)))
        pos2 = (pos1[0] + 50 * math.sin(angle), pos1[1] + 50 * math.cos(angle))
        pos3 = (pos2[0] - 25 * math.cos(angle), pos2[1] + 25 * math.sin(angle))
        pos4 = (pos3[0] - 50 * math.sin(angle), pos3[1] - 50 * math.cos(angle))
        
        self.dc = wx.PaintDC(self)
        self.dc.SetBrush(wx.Brush('#000000'))
        
        self.dc.DrawPolygon([pos1, pos2, pos3, pos4])
        
        pos1 = (pos2[0] - self.roverStatus.throttle/2 * math.sin(angle), pos2[1] - self.roverStatus.throttle/2 * math.cos(angle))
        pos4 = (pos3[0] - self.roverStatus.throttle/2 * math.sin(angle), pos3[1] - self.roverStatus.throttle/2 * math.cos(angle))

        self.dc.SetBrush(wx.Brush('#00ff00'))
        
        self.dc.DrawPolygon([pos1,pos2,pos3,pos4])
        '''
class Gui(wx.Frame):
    
    def __init__(self, parent, title):
        
        wx.Frame.__init__(self, parent, wx.ID_ANY, size=(500, 320))
        
        self.InitUI()
        self.Centre()
        self.Show()
        
    def InitUI(self):
        
        self.wheelChange = [0];
        
        self.wheelDiagram = WheelDiagram(self)

        self.angleSpin = wx.SpinCtrl(self, value='0', size=(60, -1))
        self.angleSpin.SetRange(-90, 90)
        
        self.throttleSpin = wx.SpinCtrl(self, value='0', size=(60, -1))
        self.throttleSpin.SetRange(0, 100)
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        vSizer = wx.BoxSizer(wx.VERTICAL)
        
        vSizer.Add(self.angleSpin, flag=wx.FIXED_MINSIZE)
        vSizer.Add(self.throttleSpin, flag=wx.FIXED_MINSIZE)
        
        sizer.Add(vSizer, flag=wx.FIXED_MINSIZE)
        sizer.Add(self.wheelDiagram, flag=wx.FIXED_MINSIZE)
        
        self.SetSizer(sizer)
        
    def OnSpinCtrl(self, e):
        obj = e.GetEventObject()
        if obj == self.angleSpin:
            self.wheelDiagram.set_angle(obj.GetValue(), self.wheelChange)
        elif obj == self.throttleSpin:
            self.wheelDiagram.throttle = obj.GetValue()
            self.Refresh()


if __name__ == '__main__':
    app = wx.App()
    Gui(None, 'Rover Wheel Vector Position')
    app.MainLoop()
    '''
