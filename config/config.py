import os
import configparser

from utils import Info
from utils import Error

CONFIG_PATH = "config/config.ini"
COMMON_SECTION = "Comun"


class ConfigModule:

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._read()

    def _read(self):
        if not os.path.isfile(CONFIG_PATH):
            Error("{} file not present.".format(CONFIG_PATH))
            return

        Info("Reading {} data.".format(CONFIG_PATH))
        self._config.read(CONFIG_PATH)

        if not COMMON_SECTION in self._config:
            Error("Section {} does not exist.".format(COMMON_SECTION))
    
    def GetData(self, ini_key):
        value = self._config[COMMON_SECTION].get(ini_key)
        Info("Reading {}/{} from .ini file: {}".format(COMMON_SECTION, ini_key, value))
        return value

