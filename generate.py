import wx

from config.config import ConfigModule
from data.parser import DBFParserIesiri
from data.parser import DBFParserIntrari
from data.parser import DBFParserProduse

from gui.frame import MainFrame

from utils import Info


if __name__ == "__main__":
    config = ConfigModule()
    ini_keys = ["Intrari", "Produse", "Iesiri"]
    for key in ini_keys:
        config.GetData(key)
    """
    parser_iesiri = DBFParserIesiri(config.GetData("Iesiri"))
    parser_intrari = DBFParserIntrari(config.GetData("Intrari"))
    parser_produse = DBFParserProduse(config.GetData("Produse"))

    Info("Updating Intrari data with Produse.")
    for produs in parser_produse.GetRecordData():
        intrare = parser_intrari.GetRecord(produs.id_intrare)
        intrare.AddProduct(produs)
    
    for intrare in parser_intrari.GetRecordsFromDate("20200810"):
        intrare.pprint()
    """
    app = wx.App()
    frm = MainFrame(None, title="Generator Rapoarte")
    frm.Show()
    app.MainLoop()