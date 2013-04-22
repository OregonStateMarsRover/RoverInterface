import time
from threading import *
import wx

# Define notification event for thread completion
EVT_UPDATE_ID = wx.NewId()

# Define Result Event
def EVT_UPDATE(win, func):
    win.Connect(-1, -1, EVT_UPDATE_ID, func)

class UpdaterEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATE_ID)

class UpdaterThread(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self.start()

    def run(self):
        while 1:
            time.sleep(1)
            wx.PostEvent(self._notify_window, UpdaterEvent())

# GUI Frame class that spins off the updater thread
class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Thread Test')

        # Set up event handler for any updater thread results
        EVT_UPDATE(self, self.OnUpdate)

        # Start auto-updating thread
        self.updater = UpdaterThread(self)

        # Start a counter for updating
        self.updateNum = 0

    def OnUpdate(self, event):
        print self.updateNum
        self.updateNum = self.updateNum + 1

class MainApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()