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
from drive_module import *

class AllTerrain(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        gps = wx.StaticText(self, -1, "GPS", size=(690, 690))
        gps.SetForegroundColour('white')
        driveSim = wx.StaticText(self, -1, "Drive Sim", size=(640, 443))
        driveSim.SetForegroundColour('white')
        driveControls = DriveControls(self, -1)
        tripodControls = TripodControls(self)
        
        sizer = wx.GridBagSizer(3, 3)
        
        sizer.Add(gps, (0, 0), span=(2, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(driveSim, (0, 2), span=(1, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(driveControls, (1, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(tripodControls, (1, 3), flag=wx.FIXED_MINSIZE)
        
        self.SetSizer(sizer)


class Science(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        gps = wx.StaticText(self, -1, "GPS", size=(440, 420))
        gps.SetForegroundColour('white')
        armSim = ArmSim(self, (320, 320))
        driveSim = wx.StaticText(self, -1, "Drive Sim", size=(320, 420))
        driveSim.SetForegroundColour('white')
        driveControls = DriveControls(self, -1)
        armControls = ArmControls(self, armSim)
        tripodControls = TripodControls(self)
        probeDisplay = ProbeDisplay(self)
        
        sizer = wx.GridBagSizer(3, 3)
        
        sizer.Add(gps, (0, 0), span=(1, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(armSim, (0, 3), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(driveSim, (0, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(driveControls, (2, 0), flag=wx.FIXED_MINSIZE)
        sizer.Add(armControls, (2, 1), flag=wx.FIXED_MINSIZE)
        sizer.Add(tripodControls, (2, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(probeDisplay, (2, 3), flag=wx.FIXED_MINSIZE)
        
        self.SetSizer(sizer)


class AstroRescue(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        gps = wx.StaticText(self, -1, "GPS", size=(690, 443))
        gps.SetForegroundColour('white')
        driveSim = wx.StaticText(self, -1, "Drive Sim", size=(640, 443))
        driveSim.SetForegroundColour('white')
        driveControls = DriveControls(self, -1)
        tripodControls = TripodControls(self)
        packageControls = wx.StaticText(self, -1, "Package Controls", size=(320, 250))
        packageControls.SetForegroundColour('white')
        
        sizer = wx.GridBagSizer(3, 3)
        
        sizer.Add(gps, (0, 0), span=(1, 2), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(driveSim, (0, 2), span=(1, 3), flag=wx.FIXED_MINSIZE)
        sizer.Add(driveControls, (1, 0), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(tripodControls, (1, 1), span=(1, 3), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(packageControls, (1, 4), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetSizer(sizer)


class EquipService(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        
        arm_sim = ArmSim(self, (440, 443))
        driveSim = wx.StaticText(self, -1, "Drive Sim", size=(840, 443))
        driveSim.SetForegroundColour('white')
        arm_controls = ArmControls(self, arm_sim)
        tripod_controls = TripodControls(self)
        driveControls = DriveControls(self, -1)
        
        sizer = wx.GridBagSizer(3, 3)
        
        sizer.Add(arm_sim, (0, 0),span=(1, 2), flag=wx.FIXED_MINSIZE)
        sizer.Add(driveSim, (0, 2),span=(1, 3), flag=wx.FIXED_MINSIZE)
        sizer.Add(arm_controls, (1, 0), span=(1, 2), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(tripod_controls, (1, 2), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(driveControls, (1, 3), span=(1, 2), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetSizer(sizer)


class RoverNotebook(wx.Notebook):

    def __init__(self, parent):
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
        
        self.AddPage(tabOne, "All-Terrain")
        self.AddPage(tabTwo, "Science")
        self.AddPage(tabThree, "Astronaut Rescue")
        self.AddPage(tabFour, "Equipment Servicing")


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
