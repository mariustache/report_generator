import wx
import wx.adv
import pandas as pd

from data.generator import JournalGenerator
from data.generator import ManagementGenerator
from utils import Info
from utils import Error


class MainFrame(wx.Frame):

    DATE_BUTTON = "Selecteaza data"
    MGMT_BUTTON = "Raport de gestiune"
    JOURNAL_BUTTON = "Jurnal de incasari si plati"
    BUTTONS = [DATE_BUTTON, MGMT_BUTTON, JOURNAL_BUTTON]

    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self._current_date = wx.DateTime.Now()

        self.CreateMenuBar()
        self.CreatePanels()
        self.CreateButtons()
        self.CreateTextBoxes()
        self.CreateGridBag()

        self.BindButtons()
        self.AddBorder()

    def CreateMenuBar(self):
        pass # TODO

    def CreatePanels(self):
        self.buttonPanel = wx.Panel(self)

    def CreateGridBag(self):
        self.grid = wx.GridBagSizer(3, 1)
        self.grid.Add(self.date_button, (0, 0), flag=wx.EXPAND)
        self.grid.Add(self.management_button, (1, 0), flag=wx.EXPAND)
        self.grid.Add(self.journal_button, (2, 0), flag=wx.EXPAND)
        self.grid.Add(self.crtDateText, (0, 1))

    def CreateButtons(self):
        self.date_button = wx.Button(self.buttonPanel, 0, MainFrame.DATE_BUTTON)
        self.management_button = wx.Button(self.buttonPanel, 1, MainFrame.MGMT_BUTTON)
        self.journal_button = wx.Button(self.buttonPanel, 2, MainFrame.JOURNAL_BUTTON)

        self.DisableReportButtons()
    
    def BindButtons(self):
        self.date_button.Bind(wx.EVT_BUTTON, self.OnDateButton)
        self.management_button.Bind(wx.EVT_BUTTON, self.OnManagementButton)
        self.journal_button.Bind(wx.EVT_BUTTON, self.OnJournalButton)

    def AddBorder(self):
        self.border = wx.BoxSizer()
        self.border.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)
        self.buttonPanel.SetSizerAndFit(self.border)

    def CreateTextBoxes(self):
        self.crtDateText = wx.StaticText(self.buttonPanel)

    def OnDateButton(self, event):
        calendarFrame = Calendar(self, None, title="Calendar")
        
    def OnManagementButton(self, event):
        ManagementGenerator.Instance().Generate(self._current_date, sold_precedent=41160.21)
        Info("Generated management report.")
        infoDialog = wx.MessageDialog(self, "Raportul de gestiune a fost generat.", style=wx.OK)
        infoDialog.ShowModal()
        
    def OnJournalButton(self, event):
        JournalGenerator.Instance().Generate(self._current_date, plati_numerar=165370.82, plati_alte=8320.04, incasari=192189.86)
        Info("Generated input/output journal.")
        infoDialog = wx.MessageDialog(self, "Jurnalul de incasari si plati a fost generat.", style=wx.OK)
        infoDialog.ShowModal()

    def SetCurrentDate(self, date_val):
        if date_val.IsLaterThan(wx.DateTime.Now()):
            color = wx.Colour(255, 0, 0)
            warningDateDialog = wx.MessageDialog(self, "Data selectata depaseste ziua curenta.", style=wx.OK)
            warningDateDialog.ShowModal()
            self.DisableReportButtons()
        else:
            color = wx.StaticText.GetClassDefaultAttributes().colFg
            self.EnableReportButtons()

        self.crtDateText.SetForegroundColour(color)
        self.crtDateText.SetLabel(date_val.Format("%d-%m-%Y"))
        
        self._current_date = pd.to_datetime(date_val.Format("%Y%m%d"))
        Info("Current date: {}.".format(self._current_date))

    def DisableReportButtons(self):
        self.management_button.Disable()
        self.journal_button.Disable()

    def EnableReportButtons(self):
        self.management_button.Enable()
        self.journal_button.Enable()


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


