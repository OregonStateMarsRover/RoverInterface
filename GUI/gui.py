##############################
#Program Filename: gui.py
#Author: Cameron Bowie
#Date: 1/12/2013
#Description: Organizes control and display modules into four tabs
##############################

import wx
from arm_module import *
from science_module import *
from tripod_module import *

class AllTerrain(wx.Panel):

	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		
		module1 = ArmSim(self,(320,320))
		module2 = ArmControls(self,module1)
		module3 = ProbeDisplay(self)
		module4 = ArmSim(self,(320,320))
		module5 = TripodControls(self)
		
		sizer = wx.GridBagSizer(3,3)
		
		sizer.Add(module1, (1,0), flag=wx.FIXED_MINSIZE)
		sizer.Add(module2, (0,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module3, (0,2), flag=wx.FIXED_MINSIZE)
		sizer.Add(module4, (1,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module5, (1,2), flag=wx.FIXED_MINSIZE)
		
		self.SetSizer(sizer)


class Science(wx.Panel):

	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		
		module1 = ArmSim(self,(320,320))
		module2 = ArmControls(self,module1)
		module3 = ProbeDisplay(self)
		module4 = ArmSim(self,(320,320))
		module5 = TripodControls(self)
		
		sizer = wx.GridBagSizer(3,3)
		
		sizer.Add(module1, (1,0), flag=wx.FIXED_MINSIZE)
		sizer.Add(module2, (0,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module3, (0,2), flag=wx.FIXED_MINSIZE)
		sizer.Add(module4, (1,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module5, (1,2), flag=wx.FIXED_MINSIZE)
		
		self.SetSizer(sizer)


class AstroRescue(wx.Panel):

	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		
		module1 = ArmSim(self,(320,320))
		module2 = ArmControls(self,module1)
		module3 = ProbeDisplay(self)
		module4 = ArmSim(self,(320,320))
		module5 = TripodControls(self)
		module6 = ProbeDisplay(self)
		
		sizer = wx.GridBagSizer(3,3)
		
		sizer.Add(module1, (1,0), flag=wx.FIXED_MINSIZE)
		sizer.Add(module2, (0,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module3, (0,2), flag=wx.FIXED_MINSIZE)
		sizer.Add(module4, (1,1), flag=wx.FIXED_MINSIZE)
		sizer.Add(module5, (1,2), flag=wx.FIXED_MINSIZE)
		sizer.Add(module6, (0,3), flag=wx.FIXED_MINSIZE)
		
		self.SetSizer(sizer)


class EquipService(wx.Panel):

	def __init__(self,parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		
		
		arm_sim = ArmSim(self,(440,440))
		arm_controls = ArmControls(self,arm_sim)
		tripod_controls = TripodControls(self)
		
		sizer = wx.GridBagSizer(3,3)
		
		sizer.Add(arm_sim, (0,0),span=(1,3), flag=wx.FIXED_MINSIZE)
		sizer.Add(arm_controls, (1, 2),span=(1,2), flag=wx.FIXED_MINSIZE)
		sizer.Add(tripod_controls, (1, 4), flag=wx.FIXED_MINSIZE)
		
		self.SetSizer(sizer)


class RoverNotebook(wx.Notebook):

	def __init__(self,parent):
		wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT)
		
		tabOne = AllTerrain(self)
		tabOne.SetBackgroundColour("Black")
		tabTwo = Science(self)
		tabTwo.SetBackgroundColour("Black")
		tabThree = AstroRescue(self)
		tabThree.SetBackgroundColour("Black")
		tabFour = EquipService(self)
		tabFour.SetBackgroundColour("Black")
		
		self.AddPage(tabOne,"All-Terrain")
		self.AddPage(tabTwo,"Science")
		self.AddPage(tabThree,"Astronaut Rescue")
		self.AddPage(tabFour,"Equipment Servicing")


class Gui(wx.Frame):

	def __init__(self,parent,title):
		wx.Frame.__init__(self,parent,wx.ID_ANY,title)
		
		self.InitUI()
		self.Centre()
		self.Maximize()
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
