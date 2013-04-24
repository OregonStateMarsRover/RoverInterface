#!/usr/bin/python
#-*- coding: utf-8 -*-

#cameracontrol.py

import wx


class TripodControls(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self,parent,id=wx.ID_ANY, size=(320, 250), style=wx.BORDER_SUNKEN)

        sizer = wx.GridBagSizer(3,3)
        
        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.roverStatus = roverStatus
        
        self.vOrientation = wx.Slider(self, value=self.roverStatus.tri_vert, minValue=-100, maxValue=100, size=(-1, 130), style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.hOrientation = wx.Slider(self, value=self.roverStatus.tri_hori, minValue=-100, maxValue=100, size=(140, -1), style=wx.SL_HORIZONTAL)
        self.zoom = wx.Slider(self, value=self.roverStatus.tri_zoom, minValue=0, maxValue=100, size=(-1, 40), style=wx.SL_VERTICAL|wx.SL_INVERSE)
            
        self.vOrientation.Bind(wx.EVT_SCROLL, self.ChangeValue)
        self.hOrientation.Bind(wx.EVT_SCROLL, self.ChangeValue)
        self.zoom.Bind(wx.EVT_SCROLL, self.ChangeValue)
        
        self.spinVOri = wx.SpinCtrl(self, value="%d" % self.roverStatus.tri_vert, size=(55, -1))
        self.spinHOri = wx.SpinCtrl(self, value="%d" % self.roverStatus.tri_hori, size=(55, -1))
        self.spinZoom = wx.SpinCtrl(self, value="%d" % self.roverStatus.tri_zoom, size=(55, -1))
        self.muxCamDropDown = wx.ComboBox(self, -1, size=(150, -1), choices=self.roverStatus.mux_cam_choices, style=wx.CB_DROPDOWN)
            
        self.spinVOri.SetRange(-100, 100)
        self.spinHOri.SetRange(-100, 100)
        self.spinZoom.SetRange(0, 100)
        
        self.spinVOri.Bind(wx.EVT_SPINCTRL, self.ChangeValue)
        self.spinHOri.Bind(wx.EVT_SPINCTRL, self.ChangeValue)
        self.spinZoom.Bind(wx.EVT_SPINCTRL, self.ChangeValue)
        self.muxCamDropDown.Bind(wx.EVT_COMBOBOX, self.ChangeMuxCam)
        
        stTripodControls = wx.StaticText(self, label="Tripod Controls")
        stTripodControls.SetFont(titleFont)
        stVertical = wx.StaticText(self, label="V\ne\nr\nt\ni\nc\na\nl")
        stHorizontal = wx.StaticText(self, label="Horizontal")
        stZoom = wx.StaticText(self, label="Zoom")
        stMuxCam = wx.StaticText(self, label="Camera")
        
        sizer.Add(stTripodControls, (0, 1), span=(1, 7), flag=wx.ALIGN_CENTER)
        sizer.Add(stVertical, (1, 7), span=(5, 1))
        sizer.Add(stHorizontal, (2, 1), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(stZoom, (4, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(stMuxCam, (6, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(self.vOrientation, (1, 6), span=(5, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.hOrientation, (3, 1), span=(1, 3))
        sizer.Add(self.zoom, (4, 2))
        
        sizer.Add(self.spinVOri, (6, 6))
        sizer.Add(self.spinHOri, (2, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.spinZoom, (4, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.muxCamDropDown, (7, 1), span=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(sizer)
    
    def OnPaint(self, e):
        self.spinVOri.SetValue(self.roverStatus.tri_vert)
        self.vOrientation.SetValue(self.roverStatus.tri_vert)
        self.spinHOri.SetValue(self.roverStatus.tri_hori)
        self.hOrientation.SetValue(self.roverStatus.tri_hori)
        self.spinZoom.SetValue(self.roverStatus.tri_zoom)
        self.zoom.SetValue(self.roverStatus.tri_zoom)
        mux_cam = self.roverStatus.mux_cam - 1
        mux_cam = self.roverStatus.mux_cam_choices[mux_cam]
        self.muxCamDropDown.SetValue(mux_cam)
    
    def ChangeValue(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        
        if obj == self.spinVOri or obj == self.vOrientation:
            self.roverStatus.tri_vert = value
            self.spinVOri.SetValue(value)
            self.vOrientation.SetValue(value)
        elif obj == self.spinHOri or obj == self.hOrientation:
            self.roverStatus.tri_hori = value
            self.spinHOri.SetValue(value)
            self.hOrientation.SetValue(value)
        elif obj == self.spinZoom or obj == self.zoom:
            self.roverStatus.tri_zoom = value
            self.spinZoom.SetValue(value)
            self.zoom.SetValue(value)

    def ChangeMuxCam(self, event):
        mux_cam = event.GetSelection()
        self.roverStatus.mux_cam = int(mux_cam) + 1