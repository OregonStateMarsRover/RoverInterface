##############################
#Program Filename: gui.py
#Author: Cameron Bowie
#Date: 2/6/2013
#Description: Organizes control and display modules into four tabs
##############################

import wx
from arm_module import *
from science_module import *
from tripod_module import *
from drive_module import *
from package_module import *

class AllTerrain(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        driveSim = wx.Panel(self, size=(500, 320))
        driveSim.SetBackgroundColour("Black")
        driveSimText = wx.StaticText(driveSim, -1, "Drive Sim", pos=(220, 150))
        driveSimText.SetForegroundColour("White")
        
        driveControls = DriveControls(self)
        tripodControls = TripodControls(self)
        
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

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        
        driveSim = wx.Panel(self, size=(500, 320))
        driveSim.SetBackgroundColour("Black")
        driveSimText = wx.StaticText(driveSim, -1, "Drive Sim", pos=(220, 150))
        driveSimText.SetForegroundColour("White")
        
        armSim = ArmSim(self, (320, 320))
        driveControls = DriveControls(self)
        armControls = ArmControls(self, armSim)
        tripodControls = TripodControls(self)
        probeDisplay = ProbeDisplay(self)
        
        gridSizer = wx.FlexGridSizer(2, 1, 3, 3)
        
        hSizerTop = wx.BoxSizer(wx.HORIZONTAL)
        
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(armSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(armControls, proportion=0, flag=wx.FIXED_MINSIZE|wx.TOP, border=25)
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

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        driveSim = wx.Panel(self, size=(500, 320))
        driveSim.SetBackgroundColour("Black")
        driveSimText = wx.StaticText(driveSim, -1, "Drive Sim", pos=(220, 150))
        driveSimText.SetForegroundColour("White")
        
        driveControls = DriveControls(self)
        tripodControls = TripodControls(self)
        packageControls = PackageControls(self)
        
        gridSizer = wx.FlexGridSizer(2, 1, 3, 3)
        
        hSizerTop = wx.BoxSizer(wx.HORIZONTAL)
        
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveSim, flag=wx.FIXED_MINSIZE)
        hSizerTop.Add(wx.Panel(self), proportion=1)
        hSizerTop.Add(driveControls, flag=wx.FIXED_MINSIZE|wx.TOP, border=35)
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

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        driveSim = wx.Panel(self, size=(500, 320))
        driveSim.SetBackgroundColour("Black")
        driveSimText = wx.StaticText(driveSim, -1, "Drive Sim", pos=(220, 150))
        driveSimText.SetForegroundColour("White")
        
        armSim = ArmSim(self, (320, 320))
        armControls = ArmControls(self, armSim)
        tripodControls = TripodControls(self)
        driveControls = DriveControls(self)
        
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
        hSizerBottom.Add(driveControls, proportion=0, flag=wx.FIXED_MINSIZE|wx.TOP, border=10)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(tripodControls, proportion=0, flag=wx.FIXED_MINSIZE|wx.TOP, border=10)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        hSizerBottom.Add(armControls, proportion=0, flag=wx.FIXED_MINSIZE)
        hSizerBottom.Add(wx.Panel(self), proportion=1)
        gridSizer.Add(hSizerBottom, proportion=1, flag=wx.EXPAND)
        
        gridSizer.AddGrowableCol(0, 0)
        gridSizer.AddGrowableRow(0, 1)
        
        self.SetSizer(gridSizer)
        

class RoverNotebook(wx.Notebook):

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT)
        
        tabOne = AllTerrain(self)
        
        tabTwo = Science(self)
        
        tabThree = AstroRescue(self)
        
        tabFour = EquipService(self)
        
        self.AddPage(tabOne, "All-Terrain")
        self.AddPage(tabTwo, "Science")
        self.AddPage(tabThree, "Astronaut Rescue")
        self.AddPage(tabFour, "Equipment Servicing")
        

class Gui(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1250, 650))
        
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
