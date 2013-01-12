##############################
#Program Filename: gui.py
#Author: Cameron Bowie
#Date: 1/12/2013
#Description: Organizes control and display modules into four tabs
##############################

import wx
from arm_module import *
from science_module import *

class TabTest(wx.Panel):

	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		
		module1 = ArmSim(self)
		module2 = ArmControls(self,module1)
		module3 = ProbeDisplay(self)
		module4 = ArmSim(self)
		module5 = ArmControls(self,module4)
		
		sizer = wx.GridBagSizer(3,3)
		
		sizer.Add(module1, (0,0), flag=wx.FIXED_MINSIZE)
		sizer.Add(module2, (0,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module3, (0,2), flag=wx.FIXED_MINSIZE)
		sizer.Add(module4, (1,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module5, (1,2), flag=wx.FIXED_MINSIZE)
		
		self.SetSizer(sizer)


class RoverNotebook(wx.Notebook):

	def __init__(self,parent):
		wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT)
		
		tabOne = TabTest(self)
		tabOne.SetBackgroundColour("Black")
		
		self.AddPage(tabOne,"Equip Service")


class Gui(wx.Frame):

	def __init__(self,parent,title):
		wx.Frame.__init__(self,
		                 parent,
		                 wx.ID_ANY,
		                 title,
		                 size=wx.DisplaySize()
		                 )
		self.InitUI()
		self.Centre()
		self.Show()
		
	def InitUI(self):
		panel = wx.Panel(self)
		
		notebook = RoverNotebook(panel)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
		panel.SetSizer(sizer)


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = Gui(None,title='Rover Interface')
	app.MainLoop()
