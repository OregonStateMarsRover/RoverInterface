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

import wx

class Display(wx.Frame):

	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,'Soil Probe Display', size=(600,600))
		panel = wx.Panel(self)
		button = wx.Button(panel, label='Get Probe Data', pos=(10,500), size=(100,30))
		self.Bind(wx.EVT_BUTTON, self.pressbutton, button)
		self.Bind(wx.EVT_CLOSE, self.closewindow)
		
	def pressbutton(self,event):
		#This is the command to retrieve the info from the soil probe
		print "Request Temp, Moisture, and Conductivity - cmd"
		
	def closewindow(self,event):
		self.Destroy()
		
if __name__=='__main__':
	app = wx.App()
	frame = Display(parent = None, id = -1)
	frame.Show()
	app.MainLoop()