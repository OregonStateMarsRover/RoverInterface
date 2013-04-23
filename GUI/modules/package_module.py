##############################
#Program Filename: package_module.py
#Author: Cameron Bowie
#Date: 1/12/2013
#Description: Displays the package controls
##############################

import wx

class PackageControls(wx.Panel):
    
    def __init__(self, parent, roverStatus):
        
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size=(320,250), style=wx.BORDER_SUNKEN)
        
        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.roverStatus = roverStatus
        
        stPackageControls = wx.StaticText(self, label="Package Controls")
        stPackageControls.SetFont(titleFont)
        
        btn1 = wx.Button(self, label="1")
        btn2 = wx.Button(self, label="2")
        btn3 = wx.Button(self, label="3")
        btn4 = wx.Button(self, label="4")
        btn5 = wx.Button(self, label="5")
        self.pck1 = wx.TextCtrl(self, -1, size=(70, -1))
        self.pck2 = wx.TextCtrl(self, -1, size=(70, -1))
        self.pck3 = wx.TextCtrl(self, -1, size=(70, -1))
        self.pck4 = wx.TextCtrl(self, -1, size=(70, -1))
        self.pck5 = wx.TextCtrl(self, -1, size=(70, -1))
        
        btn1.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 1': self.OnButton(evt, temp))
        btn2.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 2': self.OnButton(evt, temp))
        btn3.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 3': self.OnButton(evt, temp))
        btn4.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 4': self.OnButton(evt, temp))
        btn5.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 5': self.OnButton(evt, temp))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        sizer = wx.GridBagSizer(10, 40)
        
        sizer.Add(stPackageControls, (0, 1), span=(1, 2), flag=wx.ALIGN_CENTER)
        sizer.Add(btn1, (1, 1))
        sizer.Add(btn2, (2, 1))
        sizer.Add(btn3, (3, 1))
        sizer.Add(btn4, (4, 1))
        sizer.Add(btn5, (5, 1))
        sizer.Add(self.pck1, (1, 2))
        sizer.Add(self.pck2, (2, 2))
        sizer.Add(self.pck3, (3, 2))
        sizer.Add(self.pck4, (4, 2))
        sizer.Add(self.pck5, (5, 2))
        
        self.SetSizer(sizer)
        
    def OnButton(self,e,value):
        if value == 'Button 1':
            self.roverStatus.package_one = True
        elif value == 'Button 2':
            self.roverStatus.package_two = True
        elif value == 'Button 3':
            self.roverStatus.package_three = True
        elif value == 'Button 4':
            self.roverStatus.package_four = True
        elif value == 'Button 5':
            self.roverStatus.package_five = True
    		
    def OnPaint(self, e):
        if self.roverStatus.package_one is True:
            self.pck1.SetValue("Dropped")
        elif self.roverStatus.scoop_toggle is False:
            self.pck1.SetValue("Secured")
        if self.roverStatus.package_two is True:
            self.pck2.SetValue("Dropped")
        elif self.roverStatus.scoop_toggle is False:
            self.pck2.SetValue("Secured")
        if self.roverStatus.package_three is True:
            self.pck3.SetValue("Dropped")
        elif self.roverStatus.scoop_toggle is False:
            self.pck3.SetValue("Secured")
        if self.roverStatus.package_four is True:
            self.pck4.SetValue("Dropped")
        elif self.roverStatus.scoop_toggle is False:
            self.pck4.SetValue("Secured")
        if self.roverStatus.package_five is True:
            self.pck5.SetValue("Dropped")
        elif self.roverStatus.scoop_toggle is False:
            self.pck5.SetValue("Secured")