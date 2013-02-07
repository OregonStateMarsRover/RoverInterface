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

	def __init__(self,parent):
		wx.Panel.__init__(self,parent,id=wx.ID_ANY, size=(320,250), style=wx.BORDER_SUNKEN)
		
		button = wx.Button(self, label='Get Probe Data', pos=(70,190), size=(180,30))
		self.Bind(wx.EVT_BUTTON, self.pressbutton, button)
		
		titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
		#Degree symbol unicode
		dgsymbol_u = u'\u00b0'

		#Create Static Text for the labels
		ProbeDisplayLbl = wx.StaticText(self, label="Probe Display", pos = (85, 0))
		ProbeDisplayLbl.SetFont(titleFont)
		SoilMoistureLbl = wx.StaticText(self, -1, label = "Soil Moisture (%):", pos = (45,43))
		ConductivityLbl = wx.StaticText(self, -1, label = "Conductivity (S/m):", pos = (45,73))
		SalinityLbl = wx.StaticText(self, -1, label = "Salinity (g NaCl/L):", pos = (45, 103))
		FtempLbl = wx.StaticText(self, -1, u"Temperature (%sF):" % dgsymbol_u, pos = (45, 133))
		CtempLbl = wx.StaticText(self, -1, u"Temperature (%sC):" % dgsymbol_u, pos = (45, 163))
		
		#Empty textboxes to show the data from the probe
		SoilMoistureOutput = wx.TextCtrl(self, -1, pos = (195,40))
		ConductivityOutput = wx.TextCtrl(self, -1, pos = (195,70))
		SalinityOutput = wx.TextCtrl(self, -1, pos = (195, 100))
		FtempOutput = wx.TextCtrl(self, -1, pos = (195, 130))
		CtempOutput = wx.TextCtrl(self, -1, pos = (195, 160))
		
	def pressbutton(self,event):
		#This is the command to retrieve the info from the soil probe
		print "Request Temp, Moisture, and Conductivity - cmd"
		