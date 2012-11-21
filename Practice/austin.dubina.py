import wx

class rover_gui(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Rover Window', size = (600, 480))

        panel = wx.Panel(self)
        exit_button = wx.Button(panel, label = "exit", pos = (70, 30), size = (60, 60))
        text_button = wx.Button(panel, label = "text", pos = (10, 30), size = (60, 60))        
        self.Bind(wx.EVT_BUTTON, self.closebutton, exit_button)
        self.Bind(wx.EVT_CLOSE, self.closewindow)
        self.Bind(wx.EVT_BUTTON, self.enter_text, text_button)

        self.static_text = wx.StaticText(panel, -1, "hit text button", (10, 10))
            
        
    def closebutton(self, event):
        self.Close(True)
    
    def closewindow(self, event):
        self.Destroy()
    
    def enter_text(self, event):
        box = wx.TextEntryDialog(None, "Enter some text", "Input", "defalt text")
        if box.ShowModal() == wx.ID_OK:
            answer = box.GetValue()
            self.static_text.SetLabel(answer)
        
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = rover_gui(parent = None, id = -1)
    frame.Show()
    app.MainLoop()