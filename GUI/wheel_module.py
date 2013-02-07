#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode wxPython tutorial 

This program draws a line in 
a paint event

author: Jan Bodnar
website: zetcode.com 
last edited: November 2010
"""

import wx

class wheels(wx.Frame):
    def __init__(self, parent, title):
        super(wheels, self).__init__(parent, title=title, 
            size=(450, 450))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.Show()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        
        dc.SetBrush(wx.Brush('#000000'))
        wheel1 = dc.DrawRectangle(100, 100, 40, 55)

     
        wheel2 = dc.DrawRectangle(300, 100, 40, 55)

       
        wheel3 = dc.DrawRectangle(100, 200, 40, 55)

       
        wheel4 = dc.DrawRectangle(300, 200, 40, 55)

        wheel5 = dc.DrawRectangle(100, 300, 40, 55)

        wheel6 = dc.DrawRectangle(300, 300, 40, 55)

if __name__ == '__main__':
    app = wx.App()
    wheels(None, 'Rover Wheel Vector Position')
    app.MainLoop()