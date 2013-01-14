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
	#Arm segment lengths
	LEN_ARM1 = 1.0
	LEN_ARM2 = 1.0
	LEN_ARM3 = 0.1
	
	def __init__(self,angle1,angle2,angle3):
		#This takes in the angle of each arm segment with the previous arm segment. Angle 1 is with the x-axis.
		self.angle1 = math.radians(angle1)
		self.angle2 = math.radians(angle2)
		self.angle3 = math.radians(angle3)
		
		self.findPos()
		
	def findPos(self):
		#This calculates the second and third angle joints' angle with the x-axis
		angle2 = self.angle1+self.angle2-math.pi
		angle3 = angle2+self.angle3-math.pi
		
		#This determines the position of each joint based on the angle of each joint with the x-axis
		self.pos1 = (self.LEN_ARM1*math.cos(self.angle1),
		             self.LEN_ARM1*math.sin(self.angle1))
		             
		self.pos2 = (self.LEN_ARM2*math.cos(angle2)+self.pos1[0],
		             self.LEN_ARM2*math.sin(angle2)+self.pos1[1])
		             
		self.pos3 = (self.LEN_ARM3*math.cos(angle3)+self.pos2[0],
		             self.LEN_ARM3*math.sin(angle3)+self.pos2[1])
				
	def drawArm(self):
		data = [(0,0),self.pos1,self.pos2,self.pos3]
		lines = PolyLine(data)
	
		return PlotGraphics([lines],"Arm Simulation","Distance Out","Distance Up")
	
	
class ArmSim(wx.Panel):

	def __init__(self,parent,size):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,size=size)
		#Creates the plot, sets arm angles, and plots arm
		self.canvas = PlotCanvas(self)
		self.arm = Arm(45,100,0)
		self.canvas.Draw(self.arm.drawArm(),xAxis=(0,2),yAxis=(0,2))

		gridSizer = wx.GridBagSizer(3,3)
		
		gridSizer.Add(self.canvas,(0,0),flag=wx.EXPAND)
		
		gridSizer.AddGrowableRow(0)
		gridSizer.AddGrowableCol(0)
    	
		self.SetSizer(gridSizer)

class ArmControls(wx.Panel):
	def __init__(self,parent,arm_sim):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,size=(320,250))
		
		self.arm_sim = arm_sim
		
		self.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)
	
		self.srv1 = wx.SpinCtrl(self,value='%d'%int(round(math.degrees(self.arm_sim.arm.angle1))),size=(60, -1))
		self.srv1.SetRange(0,90)
		
		self.srv2 = wx.SpinCtrl(self,value='%d'%int(round(math.degrees(self.arm_sim.arm.angle2))),size=(60, -1))
		self.srv2.SetRange(0,360)
		
		self.srv3 = wx.SpinCtrl(self,value='%d'%int(round(math.degrees(self.arm_sim.arm.angle3))),size=(60, -1))
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
		
		armTxt = wx.StaticText(self,label='Arm')
		wristTxt = wx.StaticText(self,label='Wrist')
		scoopTxt = wx.StaticText(self,label='Scoop')
		voltTxt = wx.StaticText(self,label='Voltage')
		srv1Txt = wx.StaticText(self,label='Servo 1')
		srv2Txt = wx.StaticText(self,label='Servo 2')
		srv3Txt = wx.StaticText(self,label='Servo 3')
		
		voltOutput = wx.TextCtrl(self,-1,size=(60,-1))
		
		gridSizer = wx.GridBagSizer(3,3)
		
		gridSizer.Add(self.srv1,(1,2))
		gridSizer.Add(self.srv2,(2,2))
		gridSizer.Add(self.srv3,(3,2))
	
		gridSizer.Add(btnIn,(2,3),flag=wx.EXPAND)
		gridSizer.Add(btnUp,(1,4),flag=wx.EXPAND)
		gridSizer.Add(btnOut,(2,5),flag=wx.EXPAND|wx.RIGHT,border=15)
		gridSizer.Add(btnDown,(3,4),flag=wx.EXPAND)
		
		gridSizer.Add(armTxt,(2,4),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
		gridSizer.Add(wristTxt,(6,4),flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(scoopTxt,(4,1),flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)
		gridSizer.Add(voltTxt,(6,1),flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)
		
		gridSizer.Add(srv1Txt,(1,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(srv2Txt,(2,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		gridSizer.Add(srv3Txt,(3,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		
		gridSizer.Add(voltOutput,(7,2),flag=wx.FIXED_MINSIZE)
		
		gridSizer.Add(btnWristUp, (5, 4), flag=wx.EXPAND)
		gridSizer.Add(btnWristR, (6, 5), flag=wx.EXPAND|wx.RIGHT,border=15)
		gridSizer.Add(btnWristDown, (7, 4), flag=wx.EXPAND)
		gridSizer.Add(btnWristL, (6, 3), flag=wx.EXPAND)
		
		gridSizer.Add(btnScoopO, (5, 1), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
		gridSizer.Add(btnScoopC, (5, 2), flag=wx.FIXED_MINSIZE)
		
		gridSizer.Add(btnVoltUpdate, (7, 1), flag=wx.FIXED_MINSIZE|wx.ALIGN_CENTER_HORIZONTAL)
		
		gridSizer.AddGrowableCol(0)
		gridSizer.AddGrowableCol(1)
		gridSizer.AddGrowableCol(2)
		gridSizer.AddGrowableCol(3)
		gridSizer.AddGrowableCol(4)
		gridSizer.AddGrowableCol(5)
		gridSizer.AddGrowableCol(6)
		
		self.SetSizer(gridSizer)
		
	def OnButton(self,e,value):
		print(value)
		
	def OnSpinCtrl(self,e):
		self.arm_sim.arm.angle1 = math.radians(self.srv1.GetValue())
		self.arm_sim.arm.angle2 = math.radians(self.srv2.GetValue())
		self.arm_sim.arm.angle3 = math.radians(self.srv3.GetValue())
		self.arm_sim.arm.handAngle = self.arm_sim.arm.angle1+self.arm_sim.arm.angle2+self.arm_sim.arm.angle3
		
		self.arm_sim.arm.findPos()
		self.arm_sim.canvas.Draw(self.arm_sim.arm.drawArm(),xAxis=(0,2),yAxis=(0,2))
