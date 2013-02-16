##############################
#Program Filename: gui.py
#Author: Cameron Bowie
#Date: 2/6/2013
#Description: Organizes control and display modules into four tabs
##############################

import wx
import sys
# import threading
# For running in GUI directory
sys.path.append('./modules/')
sys.path.append('../')
# For running in RoverInterface directory
sys.path.append('./GUI/modules/')
sys.path.append('./')
from arm_module import *
from science_module import *
from tripod_module import *
from drive_module import *
from package_module import *
from rover_status import *
from wheel_module import *
from receptionist import *


class AllTerrain(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        driveSim = DriveSim(self, roverStatus)
        driveControls = DriveControls(self, driveSim, roverStatus)
        tripodControls = TripodControls(self, roverStatus)

        gridSizer = wx.FlexGridSizer(2, 1, 3, 3)

        hSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerTop, proportion=1, flag=wx.EXPAND)

        hSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(driveControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(tripodControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerBottom, proportion=1, flag=wx.EXPAND)

        gridSizer.AddGrowableCol(0, 0)
        gridSizer.AddGrowableRow(0, 1)

        self.SetSizer(gridSizer)


class Science(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        driveSim = DriveSim(self, roverStatus)
        armSim = ArmSim(self, (320, 320), roverStatus)
        driveControls = DriveControls(self, driveSim, roverStatus)
        armControls = ArmControls(self, armSim, roverStatus)
        tripodControls = TripodControls(self, roverStatus)
        probeDisplay = ProbeDisplay(self, roverStatus)

        gridSizer = wx.FlexGridSizer(2, 1, 3, 3)

        hSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(armSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(armControls, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP, border=25)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerTop, proportion=1, flag=wx.EXPAND)

        hSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(driveControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(tripodControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(probeDisplay, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerBottom, proportion=1, flag=wx.EXPAND)

        gridSizer.AddGrowableCol(0, 0)
        gridSizer.AddGrowableRow(0, 1)

        self.SetSizer(gridSizer)


class AstroRescue(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        driveSim = DriveSim(self, roverStatus)
        driveControls = DriveControls(self, driveSim, roverStatus)
        tripodControls = TripodControls(self, roverStatus)
        packageControls = PackageControls(self, roverStatus)

        gridSizer = wx.FlexGridSizer(2, 1, 3, 3)

        hSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveControls, flag=wx.FIXED_MINSIZE | wx.TOP, border=35)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerTop, proportion=1, flag=wx.EXPAND)

        hSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(tripodControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(packageControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerBottom, proportion=1, flag=wx.EXPAND)

        gridSizer.AddGrowableCol(0, 0)
        gridSizer.AddGrowableRow(0, 1)

        self.SetSizer(gridSizer)


class EquipService(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        driveSim = DriveSim(self, roverStatus)
        armSim = ArmSim(self, (320, 320), roverStatus)
        armControls = ArmControls(self, armSim, roverStatus)
        tripodControls = TripodControls(self, roverStatus)
        driveControls = DriveControls(self, driveSim, roverStatus)

        gridSizer = wx.FlexGridSizer(2, 1, 3, 3)

        hSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(armSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerTop, proportion=1, flag=wx.EXPAND)

        hSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(driveControls, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP, border=10)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(tripodControls, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP, border=10)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(armControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerBottom, proportion=1, flag=wx.EXPAND)

        gridSizer.AddGrowableCol(0, 0)
        gridSizer.AddGrowableRow(0, 1)

        self.SetSizer(gridSizer)


class RoverNotebook(wx.Notebook):

    def __init__(self, parent, roverStatus):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPaint)

        tabOne = AllTerrain(self, roverStatus)

        tabTwo = Science(self, roverStatus)

        tabThree = AstroRescue(self, roverStatus)

        tabFour = EquipService(self, roverStatus)

        self.AddPage(tabOne, "All-Terrain")
        self.AddPage(tabTwo, "Science")
        self.AddPage(tabThree, "Astronaut Rescue")
        self.AddPage(tabFour, "Equipment Servicing")

    def OnPaint(self, e):
        self.Refresh()


class Gui(wx.Frame):

    roverStatus = RoverStatus()

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1250, 650))

        self.InitReceptionist()
        self.InitUI()
        self.InitJoy()
        self.Centre()
        self.Maximize()
        self.Show()

    def InitUI(self):
        print "Starting UI"
        panel = wx.Panel(self)

        notebook = RoverNotebook(panel, self.roverStatus)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

    def InitReceptionist(self):
        print "Starting Receptionist"
        self.receptionistthread = Receptionist(self.roverStatus)
        self.bus = self.receptionistthread.bus
        self.receptionistthread.start()

    def InitJoy(self):
        print "Starting JoyParser"
        self.joythread = JoyParser(self, self.bus, self.roverStatus)
        self.joythread.start()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Gui(None, title='Rover Interface')
    app.MainLoop()
