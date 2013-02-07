##############################
#Program Filename: package_module.py
#Author: Cameron Bowie
#Date: 1/12/2013
#Description: Displays the package controls
##############################

import wx

class PackageControls(wx.Panel):
    
    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size=(320,250), style=wx.BORDER_SUNKEN)
        
        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        stPackageControls = wx.StaticText(self, label="Package Controls")
        stPackageControls.SetFont(titleFont)
        
        btn1 = wx.Button(self, label="Button 1")
        btn2 = wx.Button(self, label="Button 2")
        btn3 = wx.Button(self, label="Button 3")
        btn4 = wx.Button(self, label="Button 4")
        btn5 = wx.Button(self, label="Button 5")
        btn6 = wx.Button(self, label="Button 6")
        
        btn1.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 1': self.OnButton(evt, temp))
        btn2.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 2': self.OnButton(evt, temp))
        btn3.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 3': self.OnButton(evt, temp))
        btn4.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 4': self.OnButton(evt, temp))
        btn5.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 5': self.OnButton(evt, temp))
        btn6.Bind(wx.EVT_BUTTON, lambda evt, temp='Button 6': self.OnButton(evt, temp))
        
        sizer = wx.GridBagSizer(40, 40)
        
        sizer.Add(stPackageControls, (0, 1), span=(1, 2), flag=wx.ALIGN_CENTER)
        sizer.Add(btn1, (1, 1))
        sizer.Add(btn2, (1, 2))
        sizer.Add(btn3, (2, 1))
        sizer.Add(btn4, (2, 2))
        sizer.Add(btn5, (3, 1))
        sizer.Add(btn6, (3, 2))
        
        self.SetSizer(sizer)
        
    def OnButton(self,e,value):
		print(value)
