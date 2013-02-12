# tspgui.py
# Mike Fortner

import wx
import random
from tspsolver import TSP_solver

from wx.lib.plot import PlotCanvas, PlotGraphics, PolyLine, PolyMarker

class TSP_gui(wx.Frame):

	def __init__(self, parent, title):
		super(TSP_gui, self).__init__(parent, title=title, size=(830, 700))

		self.generated = False

		self.InitUI()
		self.Centre()
		self.Show()     

	def InitUI(self):
		panel = wx.Panel(self)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox = wx.BoxSizer(wx.VERTICAL)

		self.plot = PlotCanvas(panel)
		self.plot.SetInitialSize(size=(800, 600))

		toolbox = wx.BoxSizer(wx.HORIZONTAL)
		iterate_button = wx.Button(panel, label="Iterate")
		iterate_button.Bind(wx.EVT_BUTTON, self.OnIterate)
		gen_button = wx.Button(panel, label="Generate")
		gen_button.Bind(wx.EVT_BUTTON, self.OnGen)

		self.slider = wx.Slider(panel, value=100, minValue=10, maxValue=1000)
		self.slider_label = wx.StaticText(panel, label="%s"%self.slider.GetValue())
		self.slider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)

		self.length_label = wx.StaticText(panel, label="0")

		points = zip(range(100), [random.randint(0,1000) for i in xrange(100)], [random.randint(0,1000) for i in xrange(100)])
		self.solver = TSP_solver(points)
		self.plot.Draw(self.DrawPoints([self.solver.points[i] for i in self.solver.best_path]))
		self.length_label.SetLabel("0")




		toolbox.AddMany([	(gen_button),
							(iterate_button),
							(self.length_label, 1), 
							(self.slider_label, 1), 
							(self.slider, 10, wx.EXPAND)])

		vbox.AddMany([(self.plot, 1, wx.EXPAND), (toolbox, 0, wx.EXPAND)])

		hbox.Add(vbox, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
		panel.SetSizer(hbox)

	def OnIterate(self, e):
		self.solver.iterate()
		self.plot.Draw(self.DrawGraph([self.solver.points[i] for i in self.solver.best_path]))
		self.length_label.SetLabel("%s"%self.solver.best_length)

	def OnGen(self, e):
		if self.generated: return
		self.solver.construct_greedy()
		self.plot.Draw(self.DrawGraph([self.solver.points[i] for i in self.solver.best_path]))
		self.length_label.SetLabel("%s"%self.solver.best_length)
		self.generated = True
		
	def OnSliderScroll(self, e):
		self.generated=False
		obj = e.GetEventObject()
		val = obj.GetValue()

		self.slider_label.SetLabel("%s"%val)
		points = zip(range(val), [random.randint(0,1000) for i in xrange(val)], [random.randint(0,1000) for i in xrange(val)])
		self.solver = TSP_solver(points)
		self.plot.Draw(self.DrawPoints([self.solver.points[i] for i in self.solver.best_path]))
		self.length_label.SetLabel("0")

	def DrawLines(self, points):
		line = PolyLine(points + [points[0]], colour="red")
		return PlotGraphics([line])

	def DrawPoints(self, points):
		points = PolyMarker(points, colour="blue")
		return PlotGraphics([points])

	def DrawGraph(self, points):
		line = PolyLine(points + [points[0]], colour="red")
		points = PolyMarker(points, colour="blue")
		return PlotGraphics([points, line])

if __name__ == '__main__':
	app = wx.App(redirect=True,filename="errors.txt")
	TSP_gui(None, title='tspgui.py')
	app.MainLoop()