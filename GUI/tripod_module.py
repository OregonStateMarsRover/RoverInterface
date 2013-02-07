#!/usr/bin/python
#-*- coding: utf-8 -*-

#cameracontrol.py

import wx


class TripodControls(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=wx.ID_ANY, size=(320, 250), style=wx.BORDER_SUNKEN)

        sizer = wx.GridBagSizer(3,3)
        
        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.vOrientation = wx.Slider(self, value=0, minValue=0, maxValue=100, size=(-1, 130), style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.hOrientation = wx.Slider(self, value=0, minValue=0, maxValue=100, size=(140, -1), style=wx.SL_HORIZONTAL)
        self.zoom = wx.Slider(self, value=0, minValue=0, maxValue=100, size=(-1, 40), style=wx.SL_VERTICAL|wx.SL_INVERSE)
        
        self.vOrientation.Bind(wx.EVT_SCROLL, self.DisplayValue)
        self.hOrientation.Bind(wx.EVT_SCROLL, self.DisplayValue)
        self.zoom.Bind(wx.EVT_SCROLL, self.DisplayValue)
        
        self.spinVOri = wx.SpinCtrl(self, value="0", size=(55, -1))
        self.spinHOri = wx.SpinCtrl(self, value="0", size=(55, -1))
        self.spinZoom = wx.SpinCtrl(self, value="0", size=(55, -1))
        
        self.spinVOri.SetRange(0, 100)
        self.spinHOri.SetRange(0, 100)
        self.spinZoom.SetRange(0, 100)
        
        self.spinVOri.Bind(wx.EVT_SPINCTRL, self.ChangeValue)
        self.spinHOri.Bind(wx.EVT_SPINCTRL, self.ChangeValue)
        self.spinZoom.Bind(wx.EVT_SPINCTRL, self.ChangeValue)
        
        stTripodControls = wx.StaticText(self, label="Tripod Controls")
        stTripodControls.SetFont(titleFont)
        stVertical = wx.StaticText(self, label="V\ne\nr\nt\ni\nc\na\nl")
        stHorizontal = wx.StaticText(self, label="Horizontal")
        stZoom = wx.StaticText(self, label="Zoom")
        
        sizer.Add(stTripodControls, (0, 1), span=(1, 7), flag=wx.ALIGN_CENTER)
        sizer.Add(stVertical, (1, 7), span=(5, 1))
        sizer.Add(stHorizontal, (2, 1), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(stZoom, (4, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(self.vOrientation, (1, 6), span=(5, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.hOrientation, (3, 1), span=(1, 3))
        sizer.Add(self.zoom, (4, 2))
        
        sizer.Add(self.spinVOri, (6, 6))
        sizer.Add(self.spinHOri, (2, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.spinZoom, (4, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(sizer)
        
    def DisplayValue(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        if obj == self.vOrientation:
            self.spinVOri.SetValue(value)
        elif obj == self.hOrientation:
            self.spinHOri.SetValue(value)
        elif obj == self.zoom:
            self.spinZoom.SetValue(value)

    def ChangeValue(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        
        if obj == self.spinVOri:
            self.vOrientation.SetValue(value)
        elif obj == self.spinHOri:
            self.hOrientation.SetValue(value)
        elif obj == self.spinZoom:
            self.zoom.SetValue(value)

