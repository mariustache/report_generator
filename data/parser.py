
import csv
from operator import itemgetter
from dbfread import DBF
from pandas import DataFrame

from data.struct import Iesire
from data.struct import Intrare
from data.struct import Produs

from utils import Error
from utils import Debug
from utils import Info


class DBFParser:
    
    FIELDS = list()

    def __init__(self, dbf_name):
        dbf = DBF(dbf_name)
        columns = list(self.FIELDS.keys())
        self._dataFrame = DataFrame(iter(dbf))[columns]

        # Ensure correct data type in data frame.
        for column_name, data_type in self.FIELDS.items():
            # Replace None/NaN with default value
            fill_value = ""
            if data_type == "int64" or data_type == "float64":
                fill_value = 0
            self._dataFrame[column_name].fillna(fill_value, inplace=True)
            self._dataFrame[column_name] = self._dataFrame[column_name].astype(data_type)
        # Strip whitespace
        self._dataFrame = self._dataFrame.apply(lambda x: x.str.strip() if isinstance(x, str) else x)

    def GetData(self):
        return self._dataFrame

    def PrintData(self):
        print(self._dataFrame)


class DBFParserIesiri(DBFParser):

    FIELDS = {
        "NR_IESIRE": "object",
        "ID_IESIRE": "object",
        "DENUMIRE": "object",
        "DATA": "datetime64",
        "TOTAL": "float64",
        "NR_BONURI": "int64"
    }

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)


class DBFParserIntrari(DBFParser):

    FIELDS = {
        "ID_INTRARE": "object",
        "NR_NIR": "object",
        "NR_INTRARE": "object",
        "DENUMIRE": "object",
        "DATA": "datetime64",
        "TOTAL": "float64",
        "TIP": "object"
    }

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)
    
    def GetRecordFromId(self, id_intrare):
        print(self._dataFrame["ID_INTRARE"])
        mask = self._dataFrame["ID_INTRARE"] == id_intrare
        return self._dataFrame.loc[mask]
    
    def GetRecordsFromNir(self, nr_nir):
        print(self._dataFrame["NR_NIR"])
        mask = self._dataFrame["NR_NIR"] == nr_nir
        return self._dataFrame.loc[mask]
        
    def pprint(self):
        for key in self._record_objs:
            self._record_objs[key].pprint()


class DBFParserProduse(DBFParser):

    FIELDS = {
        "ID_U": "object",
        "ID_INTRARE": "object",
        "DENUMIRE": "object",
        "DEN_GEST": "object",
        "DEN_TIP": "object",
        "TVA_ART": "object",
        "CANTITATE": "float64",
        "PRET_VANZ": "float64"
    }

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)

    
