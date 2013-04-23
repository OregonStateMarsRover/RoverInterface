"""
'Soil Probe Data Display', by Kamal Chaya
This program will display pertinent information from the
Hydra Probe II Soil Sensor to the science team.

The information displayed will be:
    -Soil Moisture (%) - Selector H
    -Conductivity (S/m) - Selector J
        -This measure of conductivity returns a temperature
         corrected value for conductivity. I should ask the
         science team if they want this one, or the other
         measure of conductivity that is not corrected for
         temperature.
    -Salinity (g NaCl/L) -
    -Temperature (Farenheight-Selector G, and Celcius-Selector F)

"""
# -*- coding: utf-8 -*-
import wx


class ProbeDisplay(wx.Panel):

    def __init__(self, parent, roverStatus):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=(320, 250), style=wx.BORDER_SUNKEN)

        button = wx.Button(self, label='Get Probe Data', pos=(180, 190), size=(120, 30))
        self.Bind(wx.EVT_BUTTON, self.pressbutton, button)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.roverStatus = roverStatus

        self.slider = wx.Slider(self, -1, 0, 0, 100, pos=(70, 200), size=(100, -1), 
                                style = wx.SL_AUTOTICKS)

        self.slider.Bind(wx.EVT_SCROLL, self.ChangeValue)

        self.sliderwheel = wx.SpinCtrl(self, value="0", size=(60, -1), pos = (10, 200))
        self.sliderwheel.Bind(wx.EVT_SPINCTRL, self.ChangeValue)

        self.slider.SetTickFreq(5, 1)

        # Degree symbol unicode
        dgsymbol_u = u'\u00b0'

        # Create Static Text for the labels
        ProbeDisplayLbl = wx.StaticText(self, label="Probe Display", pos=(85, 0))
        ProbeDisplayLbl.SetFont(titleFont)
        SoilMoistureLbl = wx.StaticText(self, -1, label="Soil Moisture (%):", pos=(45, 43))
        ConductivityLbl = wx.StaticText(self, -1, label="Conductivity (S/m):", pos=(45, 73))
        SalinityLbl = wx.StaticText(self, -1, label="Salinity (g NaCl/L):", pos=(45, 103))
        FtempLbl = wx.StaticText(self, -1, u"Temperature (%sF):" % dgsymbol_u, pos=(45, 133))
        CtempLbl = wx.StaticText(self, -1, u"Temperature (%sC):" % dgsymbol_u, pos=(45, 163))

        # Empty textboxes to show the data from the probe
        self.SoilMoistureOutput = wx.TextCtrl(self, -1, pos=(195, 40))
        self.ConductivityOutput = wx.TextCtrl(self, -1, pos=(195, 70))
        self.SalinityOutput = wx.TextCtrl(self, -1, pos=(195, 100))
        self.FtempOutput = wx.TextCtrl(self, -1, pos=(195, 130))
        self.CtempOutput = wx.TextCtrl(self, -1, pos=(195, 160))

        # Static text for the slider.
        SliderLbl = wx.StaticText(self, -1, label="Distance:", pos=(11, 180))

    def OnPaint(self, e):
        self.SoilMoistureOutput.SetValue("%s" % self.roverStatus.soil_moisture)
        self.ConductivityOutput.SetValue("%s" % self.roverStatus.conductivity)
        self.SalinityOutput.SetValue("%s" % self.roverStatus.salinity)
        self.FtempOutput.SetValue("%s" % self.roverStatus.f_temp)
        self.CtempOutput.SetValue("%s" % self.roverStatus.c_temp)
        self.sliderwheel.SetValue(self.roverStatus.probe_distance)
        self.slider.SetValue(self.roverStatus.probe_distance)


    def pressbutton(self, event):
        self.roverStatus.probe_toggle = True

        self.SoilMoistureOutput.SetValue("%s" % self.roverStatus.soil_moisture)
        self.ConductivityOutput.SetValue("%s" % self.roverStatus.conductivity)
        self.SalinityOutput.SetValue("%s" % self.roverStatus.salinity)
        self.FtempOutput.SetValue("%s" % self.roverStatus.f_temp)
        self.CtempOutput.SetValue("%s" % self.roverStatus.c_temp)

    def ChangeValue(self, event):
        obj = event.GetEventObject()
        self.roverStatus.probe_distance = obj.GetValue()
        value = self.roverStatus.probe_distance
        self.sliderwheel.SetValue(value)
        self.slider.SetValue(value)
