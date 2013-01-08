import wx
import math
from wx.lib.plot import PlotCanvas,PlotGraphics,PolyLine

class Arm():
	LEN_ARM1 = 1.0
	LEN_ARM2 = 1.0
	LEN_ARM3 = 0.1
	
	def __init__(self,angle1,angle2,angle3):
		
		self.angle1 = math.radians(angle1)
		self.angle2 = math.radians(angle2)
		self.angle3 = math.radians(angle3)
		
		self.findPos()
		
	def findPos(self):
	
		angle2 = self.angle1+self.angle2-math.pi
		angle3 = angle2+self.angle3-math.pi
	
		self.pos1 = (self.LEN_ARM1*math.cos(self.angle1),self.LEN_ARM1*math.sin(self.angle1))
		self.pos2 = (self.LEN_ARM2*math.cos(angle2)+self.pos1[0],self.LEN_ARM2*math.sin(angle2)+self.pos1[1])
		self.pos3 = (self.LEN_ARM3*math.cos(angle3)+self.pos2[0],self.LEN_ARM3*math.sin(angle3)+self.pos2[1])
				
	def drawArm(self):
		data = [(0,0),self.pos1,self.pos2,self.pos3]
		lines = PolyLine(data)
	
		return PlotGraphics([lines],"Arm Display","Distance Out","Distance Up")

class dPad(wx.Frame):
	def __init__(self,parent,title):
	
		super(dPad,self).__init__(parent,title=title,size=(500,600))
		
		self.InitUI()
		self.Centre()
		self.Show()
		
	def InitUI(self):
	
		panel = wx.Panel(self,-1)
		
		panel.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrl)

		self.canvas = PlotCanvas(panel,size=(100,100))
		self.arm = Arm(45,100,0)
		self.canvas.Draw(self.arm.drawArm(),xAxis=(0,2),yAxis=(0,2))
		
		self.srv1 = wx.SpinCtrl(panel,value='%d'%int(round(math.degrees(self.arm.angle1))),size=(60, -1))
		self.srv1.SetRange(0,90)
		self.srv2 = wx.SpinCtrl(panel,value='%d'%int(round(math.degrees(self.arm.angle2))),size=(60, -1))
		self.srv2.SetRange(0,360)
		self.srv3 = wx.SpinCtrl(panel,value='%d'%int(round(math.degrees(self.arm.angle3))),size=(60, -1))
		self.srv3.SetRange(0,360)
		
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
		
	def OnSpinCtrl(self,e):
		self.arm.angle1 = math.radians(self.srv1.GetValue())
		self.arm.angle2 = math.radians(self.srv2.GetValue())
		self.arm.angle3 = math.radians(self.srv3.GetValue())
		self.arm.handAngle = self.arm.angle1+self.arm.angle2+self.arm.angle3
		
		self.arm.findPos()
		self.canvas.Draw(self.arm.drawArm(),xAxis=(0,2),yAxis=(0,2))
		
if __name__ == '__main__':
	
	app = wx.App()
	dPad(None,title='Arm Controls')
	app.MainLoop()
