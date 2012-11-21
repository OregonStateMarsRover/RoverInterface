import wx

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "GUI Test") # A Frame is a top-level window.
s=wx.Button(frame,-1,"Yes")
frame.Show(True)     # Show the frame.
app.MainLoop()
