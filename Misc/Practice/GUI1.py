#!/usr/bin/python


import wx
class MyFrame(wx.Frame):
        def __init__(self, parent, title):
            #Make the Frame with the following specs
            wx.Frame.__init__(self, parent, title=title, size=(500,500))
            
            #Make it so you can enter text in multiple lines in the box
            self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
            self.CreateStatusBar() #Put statusbar in bottom of window

            filemenu= wx.Menu() #setup the "FIle" menu

            #Make the "Open" menu:
            menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")

            #Adding stuff to the menu via appending
            menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about the program")

            #Separate the "about" and "exit parts of the menu"
            filemenu.AppendSeparator() 
            menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")


            #Create the menu bar
            menuBar = wx.MenuBar()
            menuBar.Append(filemenu,"&File") #Add the file menu to menubar
            self.SetMenuBar(menuBar) #Add menu bar to frame

            #Set events
            self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
            self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
            self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

            self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            self.buttons = []
            for i in range(0,6):
                    self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
                    self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.control, 1, wx.EXPAND)
            self.sizer.Add(self.sizer2, 0, wx.EXPAND)

            #layoutsizers-set up the stuff before its displayed
            self.SetSizer(self.sizer) #Tells window to use the self sizer
            self.SetAutoLayout(1)     #use the sizer to position/size the components
            self.sizer.Fit(self)      #Calculate initial/final size for all components       
                      
            #This method will show the frame 
            self.Show(True)

        def OnAbout(self,e):
            dlg = wx.MessageDialog( self, "A small text editor", "About text editor", wx.OK)
            dlg.ShowModal() #Show It
            dlg.Destroy() #finally destroy it

        def OnExit(self,e):
            self.Close(True) #Close frame

        def OnOpen(self,e):
            """ Open File """
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'r')
                    self.control.SetValue(f.read())
                    f.close()
            dlg.Destroy()

        
app = wx.App(False)
frame = MyFrame(None, 'Text Editor')
app.MainLoop()

