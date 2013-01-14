#!/usr/bin/python
#-*- coding: utf-8 -*-

#cameracontrol.py

import wx


class TripodControls(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self,parent,id=wx.ID_ANY, size=(320,250))
		
		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(9)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add((-1, 25))

		hbox1 = wx.BoxSizer(wx.VERTICAL)
		st1 = wx.StaticText(self, label='Orientation')
		st1.SetFont(font)
		hbox1.Add(st1, flag=wx.RIGHT, border=8)
		btn1 = wx.Button(self, label='Up', size=(70, 30))
		hbox1.Add(btn1, flag=wx.ALIGN_TOP, border=5)
		vbox.Add(hbox1, flag=wx.CENTER, border=100)

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		btn3 = wx.Button(self, label='Left', size=(70, 30))
		hbox2.Add(btn3, flag=wx.ALIGN_LEFT, border=5)
		btn4 = wx.Button(self, label='Right', size=(70, 30))
		hbox2.Add(btn4, flag=wx.ALIGN_RIGHT, border=5)
		vbox.Add(hbox2, flag=wx.CENTER, border=10)

		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		btn2 = wx.Button(self, label='Down', size=(70, 30))
		hbox3.Add(btn2, flag=wx.ALIGN_BOTTOM, border=5)
		#btn3 = wx.Button(self, label='Left', size=(70, 30))
		#hbox1.Add(btn3, flag=wx.ALIGN_LEFT, border=5)
		#btn4 = wx.Button(self, label='Right', size=(70, 30))
		#hbox1.Add(btn4, flag=wx.ALIGN_RIGHT)
		vbox.Add(hbox3, flag=wx.CENTER, border=100)

		vbox.Add((-1, 25))

		hbox4 = wx.BoxSizer(wx.VERTICAL)
		st2 = wx.StaticText(self, label='Zoom')
		st2.SetFont(font)
		hbox4.Add(st2, flag=wx.RIGHT, border=8)
		bttn1 = wx.Button(self, label='+', size=(70, 30))
		hbox4.Add(bttn1, flag=wx.ALIGN_TOP, border=5)
		bttn2 = wx.Button(self, label='-', size=(70,30))
		hbox4.Add(bttn2, flag=wx.ALIGN_BOTTOM, border=5)
		vbox.Add(hbox4, flag=wx.CENTER, border=20)

		vbox.Add((-1, 25))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		st3 = wx.StaticText(self, label='Camera Select')
		st3.SetFont(font)
		hbox5.Add(st3, flag=wx.RIGHT, border=8)
		vbox.Add(hbox5, flag=wx.CENTER, border=20)
		cameras = ['Main', 'Pinhole 1', 'Pinhole 2', 'Pinhole 3']
		cb = wx.ComboBox(self, pos=(50, 30), choices=cameras, style=wx.CB_READONLY)

		vbox.Add(cb, flag=wx.CENTER, border=10)

		self.SetSizer(vbox)


if __name__ == '__main__':
	app = wx.App()
	Window(None, title='Camera Controls')
	app.MainLoop()
