import os
import configparser

from utils import Info
from utils import Error

CONFIG_PATH = "config/config.ini"


class ConfigModule:

    SECTIONS = ["Common", "Management", "Journal"]

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._read()

    def _read(self):
        if not os.path.isfile(CONFIG_PATH):
            Error("{} file not present.".format(CONFIG_PATH))
            return

        Info("Reading {} data.".format(CONFIG_PATH))
        self._config.read(CONFIG_PATH)

        for section in ConfigModule.SECTIONS:
            if section not in self._config:
                Error("Section {} does not exist.".format(section))
    
    def GetDataFromKey(self, section, ini_key):
        if section not in self._config:
            Error("Section {} does not exist.".format(section))
        if ini_key not in self._config[section]:
            Error("Key {} does not exist in section {}.".format(ini_key, section))
        value = self._config[section].get(ini_key)
        Info("Reading {}/{} from .ini file: {}".format(section, ini_key, value))
        return value
    
    def GetIntrari(self):
        return self.GetDataFromKey("Common", "Intrari")
    
    def GetIesiri(self):
        return self.GetDataFromKey("Common", "Iesiri")
    
    def GetProduse(self):
        return self.GetDataFromKey("Common", "Produse")

    def GetStartDate(self):
        return self.GetDataFromKey("Common", "StartDate")
    
    def GetSoldPrecedent(self):
        return self.GetDataFromKey("Management", "SoldPrecedent")

    def GetPlatiNumerar(self):
        return self.GetDataFromKey("Journal", "PlatiNumerar")

    def GetPlatiAlte(self):
        return self.GetDataFromKey("Journal", "PlatiAlte")

    def GetIncasari(self):
        return self.GetDataFromKey("Journal", "Incasari")


