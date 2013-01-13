#!/usr/bin/env python

import wx

class MyFrame(wx.Frame):
	def __init__(self,parent,title,size):
		wx.Frame.__init__(self,parent,title=title,size=size)
		myPanel=wx.Panel(self,-1)
		self.speedSlider=wx.Slider(myPanel,-1,0,0,100,(10,15),(250,-1),wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_LABELS)
		speedLabel=wx.StaticText(myPanel,-1,"Speed",(45,5),style=wx.ALIGN_CENTER)
		self.angleSlider=wx.Slider(myPanel,-1,0,0,360,(450,15),(250,-1),wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_LABELS)
		angleLabel=wx.StaticText(myPanel,-1,"Angle",(495,5),style=wx.ALIGN_CENTRE)
		self.Show(True)
	def getSpeed(self):
		return self.speedSlider.GetValue()
	def getAngle(self):
		return self.angleSlider.GetValue()




app=wx.App(True)
frame=MyFrame(None,"Hello, World!",(800,600))
app.MainLoop()
print(str(frame.getSpeed()))
print(str(frame.getAngle()))
