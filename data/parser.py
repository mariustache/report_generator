
from dbfread import DBF
from pandas import DataFrame

from utils import Error
from utils import Debug
from utils import Info


class DBFParser:
    
    FIELDS = list()
    INSTANCE = None

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

    def GetDataWithPosition(self, position):
        return self._dataFrame.loc[[position]]

    def GetDataWithValue(self, record_key, record_value):
        mask = self._dataFrame[record_key] == record_value
        return self._dataFrame.loc[mask]

    def GetDataWithDate(self, date):
        mask = self._dataFrame["DATA"] == date
        return self._dataFrame.loc[mask]

    def GetDataFromDate(self, start_date):
        mask = self._dataFrame["DATA"] >= start_date
        return self._dataFrame.loc[mask]

    def PrintData(self):
        print(self._dataFrame)

    def PrintEntry(self, position):
        print(self._dataFrame.loc[[position]])
    
    @classmethod
    def GetParser(cls):
        if cls.INSTANCE is None:
            Error("Trying to access instance of {} class, but it does not exist.".format(cls.__name__))
        return cls.INSTANCE


class DBFParserIesiri(DBFParser):

    FIELDS = {
        "NR_IESIRE": "string",
        "ID_IESIRE": "string",
        "DENUMIRE": "string",
        "DATA": "datetime64",
        "TOTAL": "float64",
        "NR_BONURI": "int64"
    }

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)
        DBFParserIesiri.INSTANCE = self


class DBFParserIntrari(DBFParser):

    FIELDS = {
        "ID_INTRARE": "string",
        "NR_NIR": "string",
        "NR_INTRARE": "string",
        "DENUMIRE": "string",
        "DATA": "datetime64",
        "TOTAL": "float64",
        "TIP": "string"
    }

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)
        DBFParserIntrari.INSTANCE = self


class DBFParserProduse(DBFParser):

    FIELDS = {
        "ID_U": "string",
        "ID_INTRARE": "string",
        "DENUMIRE": "string",
        "DEN_GEST": "string",
        "DEN_TIP": "string",
        "TVA_ART": "string",
        "CANTITATE": "float64",
        "PRET_VANZ": "float64"
    }

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)
        DBFParserProduse.INSTANCE = self
    
    def GetDataWithIdIntrare(self, id_intrare):
        mask = self._dataFrame["ID_INTRARE"] == id_intrare
        return self._dataFrame.loc[mask]

    
