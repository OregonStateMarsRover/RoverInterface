#Calculator.py

import wx
from math import *

class Calculator(wx.Frame):
	def __init__(self,parent,title):
		super(Calculator,self).__init__(parent,title=title,size=(310,170))
		
		self.InitUI()
		self.Centre()
		self.Show()
		
	def InitUI(self):
		self.dispVal = ''
		self.undo = ['']
		self.undoPos = 1
		
		menubar = wx.MenuBar()
		calcMenu = wx.Menu()
		mundo = calcMenu.Append(1,'&Undo','Undoes an action')
		mredo = calcMenu.Append(2,'&Redo','Redoes an action')
		calcMenu.AppendSeparator()
		mquit = calcMenu.Append(wx.ID_EXIT,'&Quit','Quit application')
		menubar.Append(calcMenu,'&Calculator')
		self.SetMenuBar(menubar)
		
		self.Bind(wx.EVT_MENU, self.OnRedoUndo, mundo)
		self.Bind(wx.EVT_MENU, self.OnRedoUndo, mredo)
		self.Bind(wx.EVT_MENU, self.OnQuit, mquit)
		
		panel = wx.Panel(self,-1)
		
		button_1 = wx.Button(panel,label='1')
		button_2 = wx.Button(panel,label='2')
		button_3 = wx.Button(panel,label='3')
		button_4 = wx.Button(panel,label='4')
		button_5 = wx.Button(panel,label='5')
		button_6 = wx.Button(panel,label='6')
		button_7 = wx.Button(panel,label='7')
		button_8 = wx.Button(panel,label='8')
		button_9 = wx.Button(panel,label='9')
		button_0 = wx.Button(panel,label='0')
		button_period = wx.Button(panel,label='.')
		button_percent = wx.Button(panel,label='%')
		button_divide = wx.Button(panel,label=unicode(u"\u00F7"))
		button_mult = wx.Button(panel,label='x')
		button_subtr = wx.Button(panel,label='--')
		button_add = wx.Button(panel,label='+')
		button_lpar = wx.Button(panel,label='(')
		button_rpar = wx.Button(panel,label=')')
		button_equal = wx.Button(panel,label='=')
		button_sqrt = wx.Button(panel,label=unicode(u"\u221A"))
		button_undo = wx.Button(panel,label='Undo')
		button_back = wx.Button(panel,label=unicode(u"\u21B6"))
		button_clr = wx.Button(panel,label=unicode(u"\u232B"))
		button_xsqrd = wx.Button(panel,label='x'+unicode(u"\u00B2"))
		
		button_1.Bind(wx.EVT_BUTTON, lambda evt, temp='1': self.OnButton(evt, temp))
		button_2.Bind(wx.EVT_BUTTON, lambda evt, temp='2': self.OnButton(evt, temp))
		button_3.Bind(wx.EVT_BUTTON, lambda evt, temp='3': self.OnButton(evt, temp))
		button_4.Bind(wx.EVT_BUTTON, lambda evt, temp='4': self.OnButton(evt, temp))
		button_5.Bind(wx.EVT_BUTTON, lambda evt, temp='5': self.OnButton(evt, temp))
		button_6.Bind(wx.EVT_BUTTON, lambda evt, temp='6': self.OnButton(evt, temp))
		button_7.Bind(wx.EVT_BUTTON, lambda evt, temp='7': self.OnButton(evt, temp))
		button_8.Bind(wx.EVT_BUTTON, lambda evt, temp='8': self.OnButton(evt, temp))
		button_9.Bind(wx.EVT_BUTTON, lambda evt, temp='9': self.OnButton(evt, temp))
		button_0.Bind(wx.EVT_BUTTON, lambda evt, temp='0': self.OnButton(evt, temp))
		button_period.Bind(wx.EVT_BUTTON, lambda evt, temp='.': self.OnButton(evt, temp))
		button_percent.Bind(wx.EVT_BUTTON, lambda evt, temp='%': self.OnButton(evt, temp))
		button_divide.Bind(wx.EVT_BUTTON, lambda evt, temp='/': self.OnButton(evt, temp))
		button_mult.Bind(wx.EVT_BUTTON, lambda evt, temp='*': self.OnButton(evt, temp))
		button_subtr.Bind(wx.EVT_BUTTON, lambda evt, temp='-': self.OnButton(evt, temp))
		button_add.Bind(wx.EVT_BUTTON, lambda evt, temp='+': self.OnButton(evt, temp))
		button_lpar.Bind(wx.EVT_BUTTON, lambda evt, temp='(': self.OnButton(evt, temp))
		button_rpar.Bind(wx.EVT_BUTTON, lambda evt, temp=')': self.OnButton(evt, temp))
		button_equal.Bind(wx.EVT_BUTTON, lambda evt, temp='equal': self.OnButton(evt, temp))
		button_sqrt.Bind(wx.EVT_BUTTON, lambda evt, temp='sqrt': self.OnButton(evt, temp))
		button_undo.Bind(wx.EVT_BUTTON, lambda evt, temp='undo': self.OnButton(evt, temp))
		button_back.Bind(wx.EVT_BUTTON, lambda evt, temp='back': self.OnButton(evt, temp))
		button_clr.Bind(wx.EVT_BUTTON, lambda evt, temp='clr': self.OnButton(evt, temp))
		button_xsqrd.Bind(wx.EVT_BUTTON, lambda evt, temp='**2': self.OnButton(evt, temp))
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.display = wx.TextCtrl(panel,style=wx.TE_RIGHT)
		vbox.Add(self.display,flag=wx.EXPAND|wx.ALL,border=5)
		grid = wx.GridSizer(4,6,0,0)
		grid.AddMany( [(button_7,0,wx.EXPAND),
			(button_8,0,wx.EXPAND),
			(button_9,0,wx.EXPAND),
			(button_divide,0,wx.EXPAND),
			(button_back,0,wx.EXPAND),
			(button_clr,0,wx.EXPAND),
			(button_4,0,wx.EXPAND),
			(button_5,0,wx.EXPAND),
			(button_6,0,wx.EXPAND),
			(button_mult,0,wx.EXPAND),
			(button_lpar,0,wx.EXPAND),
			(button_rpar,0,wx.EXPAND),
			(button_1,0,wx.EXPAND),
			(button_2,0,wx.EXPAND),
			(button_3,0,wx.EXPAND),
			(button_subtr,0,wx.EXPAND),
			(button_xsqrd,0,wx.EXPAND),
			(button_sqrt,0,wx.EXPAND),
			(button_0,0,wx.EXPAND),
			(button_period,0,wx.EXPAND),
			(button_percent,0,wx.EXPAND),
			(button_add,0,wx.EXPAND),
			(button_undo,0,wx.EXPAND),
			(button_equal,0,wx.EXPAND) ])

		vbox.Add(grid,proportion=1,flag=wx.EXPAND)
		panel.SetSizer(vbox)
	
	def OnRedoUndo(self,e):
		if e.GetId() == 1:
			self.OnButton(e,'undo')
		elif e.GetId() == 2:
			self.OnButton(e,'redo')
	
	def OnQuit(self,e):
		self.Close()
	
	def OnButton(self,e,val):
		if val  == 'back':
			self.dispVal = self.dispVal[0:len(self.dispVal)-1]
		elif val  == 'clr':
			self.dispVal = ''
		elif val == 'sqrt':
			self.dispVal = 'sqrt('+ self.dispVal + ')'
		elif val == 'undo':
			if len(self.undo) >= self.undoPos > 0:
				self.undoPos -= 1
				self.dispVal = self.undo[self.undoPos]
		elif val == 'redo':
			if len(self.undo) > self.undoPos+1:
				self.undoPos += 1
				self.dispVal = self.undo[self.undoPos]
		elif val == 'equal':
			try:
				tempVal = str(eval(self.dispVal))
				if len(self.undo) == self.undoPos:
					if self.undo[-1] != self.dispVal:
						self.undo.append(self.dispVal)
						self.undoPos += 1
				else:
					self.undo = self.undo[0:self.undoPos]
					self.undo.append(self.dispVal)
					self.undoPos += 1
				self.dispVal = tempVal
			except:
				pass
		else:
			self.dispVal += val
			
		self.display.SetValue(self.dispVal)
		
if __name__ == '__main__':
	
	app = wx.App()
	Calculator(None,title='Calculator')
	app.MainLoop()
