import wx
import wx.adv

from utils import Info, Error

class MainFrame(wx.Frame):

    BUTTONS = ["Selecteaza data", "Genereaza raport de gestiune", "Genereaza jurnal de incasari si plati"]

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self._button_id = 0
        self._current_date = wx.DateTime.Now()

        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(sizer)

        self.makeMenuBar()
        self.makeButtons()

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def makeButtons(self):
        pos_x_const = 10
        pos_y = 10
        for button_name in MainFrame.BUTTONS:
            button = wx.Button(self.panel, self._button_id, button_name, wx.Point(pos_x_const, pos_y))
            button.name = button_name
            button.Bind(wx.EVT_BUTTON, self.OnButton, button)
            self._button_id += 1
            pos_y += button.GetDefaultSize().GetHeight()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)
    
    def OnButton(self, event):
        name = event.GetEventObject().name
        if name == "Selecteaza data":
            calendarFrame = Calendar(self, None, title="Calendar")
        elif name == "Genereaza raport de gestiune":
            Info("Generated management report.")
        elif name == "Genereaza jurnal de incasari si plati":
            Info("Generated input/output journal.")
        else:
            Error("Unknown event.")

    def SetCurrentDate(self, date_val):
        self._current_date = date_val
        Info("Current date: {}.".format(self._current_date))


class Calendar(wx.Frame):

    def __init__(self, parent_frame, *args, **kargs):
        wx.Frame.__init__(self, *args, **kargs)
        self.parent = parent_frame
        self.cal = wx.adv.CalendarCtrl(self, 10, wx.DateTime.Now())
        self.cal.Bind(wx.adv.EVT_CALENDAR, self.OnDate)
        self.Show()

    def OnDate(self, event):
        self.parent.SetCurrentDate(self.cal.GetDate())
        self.Close()


