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
		wx.Panel.__init__(self,parent,id=wx.ID_ANY, size=(320,250))
		
		button = wx.Button(self, label='Get Probe Data', pos=(10,190), size=(100,30))
		self.Bind(wx.EVT_BUTTON, self.pressbutton, button)
		
		#Degree symbol unicode
		dgsymbol_u = u'\u00b0'
		
		#Create read only textboxes (these are merely acting as labels)
		"""
		SoilMoistureTXTBOX = wx.TextCtrl(panel, -1, "Soil Moisture (%):", pos = (10,10), style = wx.TE_READONLY)
		ConductivityTXTBOX = wx.TextCtrl(panel, -1, "Conductivity (S/m):", pos = (10,40), style = wx.TE_READONLY)
		SalinityTXTBOX = wx.TextCtrl(panel, -1, "Salinity (g NaCl/L):", pos = (10, 70), style = wx.TE_READONLY)
		FtempTXTBOX = wx.TextCtrl(panel, -1, u"Temperature (%sF):" % dgsymbol_u, pos = (10, 100), style = wx.TE_READONLY)
		CtempTXTBOX = wx.TextCtrl(panel, -1, u"Temperature (%sC):" % dgsymbol_u, pos = (10, 130), style = wx.TE_READONLY)
		"""
		
		#Create Static Text for the labels
		SoilMoistureLbl = wx.StaticText(self, -1, label = "Soil Moisture (%):", pos = (10,10))
		ConductivityLbl = wx.StaticText(self, -1, label = "Conductivity (S/m):", pos = (10,40))
		SalinityLbl = wx.StaticText(self, -1, label = "Salinity (g NaCl/L):", pos = (10, 70))
		FtempLbl = wx.StaticText(self, -1, u"Temperature (%sF):" % dgsymbol_u, pos = (10, 100))
		CtempLbl = wx.StaticText(self, -1, u"Temperature (%sC):" % dgsymbol_u, pos = (10, 130))
		
		#Empty textboxes to show the data from the probe
		SoilMoistureOutput = wx.TextCtrl(self, -1, pos = (130,10))
		ConductivityOutput = wx.TextCtrl(self, -1, pos = (130,40))
		SalinityOutput = wx.TextCtrl(self, -1, pos = (130, 70))
		FtempOutput = wx.TextCtrl(self, -1, pos = (130, 100))
		CtempOutput = wx.TextCtrl(self, -1, pos = (130, 130))
		
	def pressbutton(self,event):
		#This is the command to retrieve the info from the soil probe
		print "Request Temp, Moisture, and Conductivity - cmd"
		
