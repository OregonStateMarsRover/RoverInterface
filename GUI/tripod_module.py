#!/usr/bin/python
#-*- coding: utf-8 -*-

#cameracontrol.py

import wx


class TripodControls(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=wx.ID_ANY, size=(320,250))
        
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        
        sizer = wx.GridBagSizer(3,3)

        stOrientation = wx.StaticText(self, label='Orientation')
        stOrientation.SetFont(font)

        btnUp = wx.Button(self, label=u"\u2191",size=(30,-1))
        btnLeft = wx.Button(self, label=u"\u2190",size=(30,-1))
        btnRight = wx.Button(self, label=u"\u2192",size=(30,-1))
        btnDown = wx.Button(self, label=u"\u2193",size=(30,-1))

        stZoom = wx.StaticText(self, label='Zoom',size=(50,-1))
        stZoom.SetFont(font)

        btnZoomIn = wx.Button(self, label='+',size=(30,-1))
        btnZoomOut = wx.Button(self, label='-',size=(30,-1))

        stCameraSelect = wx.StaticText(self, label='Camera Select')
        stCameraSelect.SetFont(font)
   
        cameras = ['Main', 'Pinhole 1', 'Pinhole 2', 'Pinhole 3']
        
        cb = wx.ComboBox(self, choices=cameras, style=wx.CB_READONLY)
        
        sizer.Add(btnUp, (1, 2), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(btnLeft, (2, 1), flag=wx.FIXED_MINSIZE)
        sizer.Add(btnDown, (3, 2), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(btnRight, (2, 3), flag=wx.FIXED_MINSIZE)
        
        sizer.Add(stOrientation, (2, 2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        
        sizer.Add(btnZoomIn, (2, 5), flag=wx.FIXED_MINSIZE)
        sizer.Add(btnZoomOut, (2, 6), flag=wx.FIXED_MINSIZE)
        
        sizer.Add(stZoom, (1, 5), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.TOP, border=15)
        
        sizer.Add(stCameraSelect, (5, 2), span=(1, 4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        
        sizer.Add(cb, (6, 2), span=(1, 5), flag=wx.FIXED_MINSIZE)
        
        self.SetSizer(sizer)

