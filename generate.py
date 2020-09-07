import wx

from config.config import ConfigModule
from data.parser import DBFParserIesiri
from data.parser import DBFParserIntrari
from data.parser import DBFParserProduse
from data.generator import JournalGenerator
from data.generator import ManagementGenerator

from gui.frame import MainFrame

from utils import Info


if __name__ == "__main__":
    config = ConfigModule()

    parser_iesiri = DBFParserIesiri(config.GetDataFromKey("Iesiri"))
    parser_intrari = DBFParserIntrari(config.GetDataFromKey("Intrari"))
    parser_produse = DBFParserProduse(config.GetDataFromKey("Produse"))

    journal_generator = JournalGenerator()
    management_generator = ManagementGenerator()
    
    app = wx.App()
    frm = MainFrame(None, title="Generator Rapoarte")
    frm.Show()
    app.MainLoop()