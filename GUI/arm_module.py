##############################
#Program Filename: arm_module.py
#Author: Cameron Bowie
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
	'''
	This class calculates and stores arm angles and positions
	'''
	target = [0,0]

	seg = [{},{},{}]
	#Arm segment lengths
	seg[0]['len'] = 1.4
	seg[1]['len'] = 1.3
	seg[2]['len'] = 1.0
	
	def __init__(self,angle1,angle2,angle3):
		#This takes in the angle of each arm segment with the previous arm segment. Angle 1 is with the x-axis.
		
		self.seg[0]['angle'] = math.radians(angle1)
		self.seg[1]['angle'] = math.radians(angle2)
		self.seg[2]['angle'] = math.radians(angle3)
		
		self.findPos()
		self.target = [self.seg[1]['pos'][0],self.seg[1]['pos'][1]]
		
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
		#This calculates the second and third angle joints' angle with the x-axis
		angle2 = self.seg[0]['angle']+self.seg[1]['angle']-math.pi
		angle3 = angle2+self.seg[2]['angle']-math.pi
		
		#This determines the position of each joint based on the angle of each joint with the x-axis
		
		self.seg[0]['pos'] = (self.seg[0]['len']*math.cos(self.seg[0]['angle']),self.seg[0]['len']*math.sin(self.seg[0]['angle']))
		self.seg[1]['pos'] = (self.seg[1]['len']*math.cos(angle2)+self.seg[0]['pos'][0],self.seg[1]['len']*math.sin(angle2)+self.seg[0]['pos'][1])
		self.seg[2]['pos'] = (self.seg[2]['len']*math.cos(angle3)+self.seg[1]['pos'][0],self.seg[2]['len']*math.sin(angle3)+self.seg[1]['pos'][1])
		
				
	def drawArm(self):
		print self.seg[0]['angle'], self.seg[1]['angle'], self.seg[2]['angle']

		self.findPos()
		data = [(0,0),self.seg[0]['pos'],self.seg[1]['pos'],self.seg[2]['pos']]
		lines = PolyLine(data)
	
		return PlotGraphics([lines],"Arm Display","Distance Out","Distance Up")

class ArmSim(wx.Panel):

	def __init__(self,parent,size):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,size=size)
		#Creates the plot, sets arm angles, and plots arm
		self.canvas = PlotCanvas(self)
		self.arm = Arm(45,100,0)
		self.canvas.Draw(self.arm.drawArm(),xAxis=(-1,4),yAxis=(-1,4))

		gridSizer = wx.GridBagSizer(3,3)
		
		gridSizer.Add(self.canvas,(0,0),flag=wx.EXPAND)
		
		gridSizer.AddGrowableRow(0)
		gridSizer.AddGrowableCol(0)
    	
		self.SetSizer(gridSizer)

class ArmControls(wx.Panel):
	def __init__(self,parent,arm_sim):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size=(320, 270), style=wx.BORDER_SUNKEN)
		
		self.arm_sim = arm_sim
		
		self.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)
	
		self.srv1 = wx.SpinCtrl(self,value='%d'%int(round(math.degrees(self.arm_sim.arm.seg[0]['angle']))),size=(60, -1))
		self.srv1.SetRange(0,90)

		self.srv2 = wx.SpinCtrl(self,value='%d'%int(round(math.degrees(self.arm_sim.arm.seg[1]['angle']))),size=(60, -1))
		self.srv2.SetRange(0,360)
		

		self.srv3 = wx.SpinCtrl(self,value='%d'%int(round(math.degrees(self.arm_sim.arm.seg[2]['angle']))),size=(60, -1))
		self.srv3.SetRange(0,360)
		
		btnIn = wx.Button(self,label=u"\u2190",size=(30,-1))
		btnUp = wx.Button(self,label=u"\u2191",size=(30,-1))
		btnOut = wx.Button(self,label=u"\u2192",size=(30,-1))
		btnDown = wx.Button(self,label=u"\u2193",size=(30,-1))
		
		btnWristUp = wx.Button(self,label=u"\u2191",size=(30,-1))
		btnWristR = wx.Button(self,label=u"\u21BB",size=(30,-1))
		btnWristDown = wx.Button(self,label=u"\u2193",size=(30,-1))
		btnWristL = wx.Button(self,label=u"\u21BA",size=(30,-1))
		
		btnScoopO = wx.Button(self,label='Open',size=(60,-1))
		btnScoopC = wx.Button(self,label='Close',size=(60,-1))
		
		btnVoltUpdate = wx.Button(self,label='Update',size=(65,-1))
    	
		btnIn.Bind(wx.EVT_BUTTON, lambda evt, temp='in': self.OnButton(evt, temp))
		btnUp.Bind(wx.EVT_BUTTON, lambda evt, temp='up': self.OnButton(evt, temp))
		btnOut.Bind(wx.EVT_BUTTON, lambda evt, temp='out': self.OnButton(evt, temp))
		btnDown.Bind(wx.EVT_BUTTON, lambda evt, temp='down': self.OnButton(evt, temp))
		btnWristUp.Bind(wx.EVT_BUTTON, lambda evt, temp='wrist up': self.OnButton(evt, temp))
		btnWristR.Bind(wx.EVT_BUTTON, lambda evt, temp='wrist right': self.OnButton(evt, temp))
		btnWristDown.Bind(wx.EVT_BUTTON, lambda evt, temp='wrist down': self.OnButton(evt, temp))
		btnWristL.Bind(wx.EVT_BUTTON, lambda evt, temp='wrist left': self.OnButton(evt, temp))
		btnScoopO.Bind(wx.EVT_BUTTON, lambda evt, temp='scoop open': self.OnButton(evt, temp))
		btnScoopC.Bind(wx.EVT_BUTTON, lambda evt, temp='scoop close': self.OnButton(evt, temp))
		btnVoltUpdate.Bind(wx.EVT_BUTTON, lambda evt, temp='voltage update': self.OnButton(evt, temp))
		
		titleFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
		titleTxt = wx.StaticText(self, label="Arm Controls")
		titleTxt.SetFont(titleFont)
		armTxt = wx.StaticText(self,label='Arm')
		wristTxt = wx.StaticText(self,label='Wrist')
		scoopTxt = wx.StaticText(self,label='Scoop')
		voltTxt = wx.StaticText(self,label='Voltage')
		srv1Txt = wx.StaticText(self,label='Servo 1')
		srv2Txt = wx.StaticText(self,label='Servo 2')
		srv3Txt = wx.StaticText(self,label='Servo 3')
		
		voltOutput = wx.TextCtrl(self,-1,size=(60,-1))
		
		gridSizer = wx.GridBagSizer(3,3)
		
		gridSizer.Add(self.srv1,(2,2))
		gridSizer.Add(self.srv2,(3,2))
		gridSizer.Add(self.srv3,(4,2))
	
		gridSizer.Add(btnIn,(3,4),flag=wx.EXPAND)
		gridSizer.Add(btnUp,(2,5),flag=wx.EXPAND)
		gridSizer.Add(btnOut,(3,6),flag=wx.EXPAND|wx.RIGHT,border=15)
		gridSizer.Add(btnDown,(4,5),flag=wx.EXPAND)
		
		gridSizer.Add(titleTxt, (0, 0), span=(1, 7), flag=wx.ALIGN_CENTER)
		gridSizer.Add(armTxt,(3,5),flag=wx.ALIGN_CENTER)
		gridSizer.Add(wristTxt,(7,5),flag=wx.ALIGN_CENTER)
		gridSizer.Add(scoopTxt,(5,1),flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)
		gridSizer.Add(voltTxt,(7,1),flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)
		
		gridSizer.Add(srv1Txt,(2,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(srv2Txt,(3,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(srv3Txt,(4,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		
		gridSizer.Add(voltOutput,(8,2),flag=wx.FIXED_MINSIZE)
		
		gridSizer.Add(btnWristUp, (6, 5), flag=wx.EXPAND)
		gridSizer.Add(btnWristR, (7, 6), flag=wx.EXPAND|wx.RIGHT,border=15)
		gridSizer.Add(btnWristDown, (8, 5), flag=wx.EXPAND)
		gridSizer.Add(btnWristL, (7, 4), flag=wx.EXPAND)
		
		gridSizer.Add(btnScoopO, (6, 1), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
		gridSizer.Add(btnScoopC, (6, 2), flag=wx.FIXED_MINSIZE)
		
		gridSizer.Add(btnVoltUpdate, (8, 1), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
		'''
		gridSizer.AddGrowableCol(0)
		gridSizer.AddGrowableCol(1)
		gridSizer.AddGrowableCol(2)
		gridSizer.AddGrowableCol(3)
		gridSizer.AddGrowableCol(4)
		gridSizer.AddGrowableCol(5)
		gridSizer.AddGrowableCol(6)
		'''
		self.SetSizer(gridSizer)
		
	def OnButton(self,e,value):
		print(value)
		self.arm_sim.arm.target = [self.arm_sim.arm.seg[1]['pos'][0],self.arm_sim.arm.seg[1]['pos'][1]]

		if value == 'up':
			print '^'
			self.arm_sim.arm.target[1] += .01
		elif value == 'down':
			print 'v'
			self.arm_sim.arm.target[1] -= .01
		elif value == 'in':
			print '<'
			self.arm_sim.arm.target[0] -= .01
		elif value == 'out':
			print '>'
			self.arm_sim.arm.target[0] += .01
		for x in xrange(1,30):
			self.arm_sim.arm.reach()

		self.srv1.SetValue(math.degrees(self.arm_sim.arm.seg[0]['angle']))
		self.srv2.SetValue(math.degrees(self.arm_sim.arm.seg[1]['angle']))
		self.srv3.SetValue(math.degrees(self.arm_sim.arm.seg[2]['angle']))

		self.arm_sim.canvas.Draw(self.arm_sim.arm.drawArm(),xAxis=(-1,4),yAxis=(-1,4))

		
	def OnSpinCtrl(self,e):
		self.arm_sim.arm.seg[0]['angle'] = math.radians(self.srv1.GetValue())
		self.arm_sim.arm.seg[1]['angle'] = math.radians(self.srv2.GetValue())
		self.arm_sim.arm.seg[2]['angle'] = math.radians(self.srv3.GetValue())
		self.arm_sim.arm.handAngle = self.arm_sim.arm.seg[0]['angle']+self.arm_sim.arm.seg[1]['angle']+self.arm_sim.arm.seg[2]['angle']
		
		self.arm_sim.arm.findPos()
		self.arm_sim.canvas.Draw(self.arm_sim.arm.drawArm(),xAxis=(-1,4),yAxis=(-1,4))
