##############################
#Program Filename: arm_module.py
#Author: Cameron Bowie and Francis Vo
#Date: 1/12/2013
#Description: Contains three classes- Arm, ArmSim, and ArmControls.
#		-Arm(): Stores variables for the arm simulation and has methods that calculate the position of joints and draw the arm
#		-ArmSim(wx.Panel): Generates plot for arm and calls draw command for arm
#		-ArmControls(wx.Panel): Generates controls for the arm 
##############################

import wx
import math
from wx.lib.plot import PlotCanvas,PlotGraphics,PolyLine

class Arm():
	target = [0,0]

	seg = [{},{},{}]
	#Arm segment lengths
	seg[0]['len'] = 1.4
	seg[1]['len'] = 1.3
	seg[2]['len'] = 1.0
	
	def __init__(self,angle1,angle2,angle3):
		self.seg[0]['angle'] = math.radians(angle1)
		self.seg[1]['angle'] = math.radians(angle2)
		self.seg[2]['angle'] = math.radians(angle3)
		
		self.findPos()
		target = [self.seg[1]['pos'][0],self.seg[1]['pos'][1]]
	
	def reach(self):
		angle2 = self.seg[0]['angle']+self.seg[1]['angle']-math.pi
		angle3 = angle2+self.seg[2]['angle']-math.pi

		dx = self.target[0] - self.seg[0]['pos'][0]
		dy = self.target[1] - self.seg[0]['pos'][1]
		da = math.atan2(dy, dx) - angle2
		angle2 += da/2
		self.seg[1]['angle'] = angle2 - self.seg[0]['angle'] + math.pi

		dx = self.target[0] - math.cos(angle2) * self.seg[1]['len']
		dy = self.target[1] - math.sin(angle2) * self.seg[1]['len']
		da = math.atan2(dy, dx) - self.seg[0]['angle']
		self.seg[0]['angle'] += da
		math.degrees(self.seg[0]['angle'])


		self.seg[2]['angle'] = angle3 - angle2 + math.pi

	def findPos(self):
	
		angle2 = self.seg[0]['angle']+self.seg[1]['angle']-math.pi
		angle3 = angle2+self.seg[2]['angle']-math.pi

	
		self.seg[0]['pos'] = (self.seg[0]['len']*math.cos(self.seg[0]['angle']),self.seg[0]['len']*math.sin(self.seg[0]['angle']))
		self.seg[1]['pos'] = (self.seg[1]['len']*math.cos(angle2)+self.seg[0]['pos'][0],self.seg[1]['len']*math.sin(angle2)+self.seg[0]['pos'][1])
		self.seg[2]['pos'] = (self.seg[2]['len']*math.cos(angle3)+self.seg[1]['pos'][0],self.seg[2]['len']*math.sin(angle3)+self.seg[1]['pos'][1])
				
	def drawArm(self):
		print self.seg[0]['angle'], self.seg[1]['angle'], self.seg[2]['angle']

		self.findPos()
		data = [(0,0),self.seg[0]['pos'],self.seg[1]['pos'],self.seg[2]['pos']]
		lines = PolyLine(data)
	
		return PlotGraphics([lines],"Arm Display","Distance Out","Distance Up")

class dPad(wx.Frame):
	def __init__(self,parent,title):
	
		super(dPad,self).__init__(parent,title=title,size=(1000,1000))
		
		self.InitUI()
		self.Centre()
		self.Show()
		
	def InitUI(self):
	
		panel = wx.Panel(self,-1)
		
		panel.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)

		self.canvas = PlotCanvas(panel,size=(400,400))
		self.arm = Arm(45,100,250)
		self.canvas.Draw(self.arm.drawArm(),xAxis=(-4,4),yAxis=(-4,4))
		
		self.srv1 = wx.SpinCtrl(panel,value='%d'%int(round(math.degrees(self.arm.seg[0]['angle']))),size=(60, -1))
		self.srv1.SetRange(0,90)
		self.srv2 = wx.SpinCtrl(panel,value='%d'%int(round(math.degrees(self.arm.seg[1]['angle']))),size=(60, -1))
		self.srv2.SetRange(0,360)
		print int(round(math.degrees(self.arm.seg[2]['angle'])))
		self.srv3 = wx.SpinCtrl(panel,value='%d'%int(round(math.degrees(self.arm.seg[2]['angle']))),size=(60, -1))
		self.srv3.SetRange(0,360)
		self.srv3.SetValue(int(round(math.degrees(self.arm.seg[2]['angle']))))
		
		btnIn = wx.Button(panel,label=u"\u2190",size=(30,20))
		btnUp = wx.Button(panel,label=u"\u2191",size=(30,20))
		btnOut = wx.Button(panel,label=u"\u2192",size=(30,20))
		btnDown = wx.Button(panel,label=u"\u2193",size=(30,20))
		btnStop = wx.Button(panel,label='Stop',size=(30,20))
		
		btnWristR = wx.Button(panel,label=u"\u21BB")
		btnWristL = wx.Button(panel,label=u"\u21BA")
		
		btnScoopO = wx.Button(panel,label='Open')
		btnScoopC = wx.Button(panel,label='Close')
    	
		btnIn.Bind(wx.EVT_BUTTON, lambda evt, temp='in': self.OnButton(evt, temp))
		btnUp.Bind(wx.EVT_BUTTON, lambda evt, temp='up': self.OnButton(evt, temp))
		btnOut.Bind(wx.EVT_BUTTON, lambda evt, temp='out': self.OnButton(evt, temp))
		btnDown.Bind(wx.EVT_BUTTON, lambda evt, temp='down': self.OnButton(evt, temp))
		btnStop.Bind(wx.EVT_BUTTON, lambda evt, temp='stop': self.OnButton(evt, temp))
		btnWristR.Bind(wx.EVT_BUTTON, lambda evt, temp='wrist right': self.OnButton(evt, temp))
		btnWristL.Bind(wx.EVT_BUTTON, lambda evt, temp='wrist left': self.OnButton(evt, temp))
		btnScoopO.Bind(wx.EVT_BUTTON, lambda evt, temp='scoop open': self.OnButton(evt, temp))
		btnScoopC.Bind(wx.EVT_BUTTON, lambda evt, temp='scoop close': self.OnButton(evt, temp))
		
		armTxt = wx.StaticText(panel,label='Arm')
		wristTxt = wx.StaticText(panel,label='Wrist')
		scoopTxt = wx.StaticText(panel,label='Scoop')
		srv1Txt = wx.StaticText(panel,label='Servo 1')
		srv2Txt = wx.StaticText(panel,label='Servo 2')
		srv3Txt = wx.StaticText(panel,label='Servo 3')
		
		gridSizer = wx.GridBagSizer(3,3)
		
		gridSizer.Add(self.srv1,(6,1))
		gridSizer.Add(self.srv2,(7,1))
		gridSizer.Add(self.srv3,(8,1))
		
		gridSizer.Add(self.canvas,(0,0),span=(5,9),flag=wx.EXPAND)
		
		gridSizer.Add(btnIn,(7,2),flag=wx.EXPAND)
		gridSizer.Add(btnUp,(6,3),flag=wx.EXPAND)
		gridSizer.Add(btnOut,(7,4),flag=wx.EXPAND)
		gridSizer.Add(btnDown,(8,3),flag=wx.EXPAND)
		gridSizer.Add(btnStop,(7,3),flag=wx.EXPAND)
		
		gridSizer.Add(armTxt,(5,2),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP,border=14)
		gridSizer.Add(wristTxt,(5,6),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP,border=14)
		gridSizer.Add(scoopTxt,(7,6),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP,border=14)
		
		gridSizer.Add(srv1Txt,(6,0),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(srv2Txt,(7,0),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(srv3Txt,(8,0),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		
		gridSizer.Add(btnWristR,(6,7),flag=wx.EXPAND)
		gridSizer.Add(btnWristL,(6,6),flag=wx.EXPAND)
		gridSizer.Add(btnScoopO,(8,6),flag=wx.EXPAND)
		gridSizer.Add(btnScoopC,(8,7),flag=wx.EXPAND)
    	
		gridSizer.AddGrowableRow(0)
		
		gridSizer.AddGrowableCol(0)
		
		gridSizer.AddGrowableCol(1)
		gridSizer.AddGrowableCol(2)
		gridSizer.AddGrowableCol(3)
		gridSizer.AddGrowableCol(4)
		gridSizer.AddGrowableCol(5)
		gridSizer.AddGrowableCol(6)
		
    	
		panel.SetSizer(gridSizer)
    	
	def OnButton(self,e,value):
		print(value)
		self.arm.target = [self.arm.seg[1]['pos'][0],self.arm.seg[1]['pos'][1]]

		if value == 'up':
			print '^'
			self.arm.target[1] += .01
		elif value == 'down':
			print 'v'
			self.arm.target[1] -= .01
		elif value == 'in':
			print '<'
			self.arm.target[0] -= .01
		elif value == 'out':
			print '>'
			self.arm.target[0] += .01
		for x in xrange(1,30):
			self.arm.reach()

		# self.srv1.SetValue(math.degrees(self.arm.seg[0]['angle']))
		# self.srv2.SetValue(math.degrees(self.arm.seg[1]['angle']))
		# self.srv3.SetValue(math.degrees(self.arm.seg[2]['angle']))
		self.canvas.Draw(self.arm.drawArm(),xAxis=(-4,4),yAxis=(-4,4))
		
	def OnSpinCtrl(self,e):
		self.arm.seg[0]['angle'] = math.radians(self.srv1.GetValue())
		self.arm.seg[1]['angle'] = math.radians(self.srv2.GetValue())
		self.arm.seg[2]['angle'] = math.radians(self.srv3.GetValue())
		self.arm.handAngle = self.arm.seg[0]['angle']+self.arm.seg[1]['angle']+self.arm.seg[2]['angle']
		
		self.arm.findPos()
		self.canvas.Draw(self.arm.drawArm(),xAxis=(-4,4),yAxis=(-4,4))
		
if __name__ == '__main__':
	
	app = wx.App()
	dPad(None,title='Arm Controls')
	app.MainLoop()
