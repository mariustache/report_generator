
import csv
from operator import itemgetter
from dbfread import DBF

from data.struct import Iesire
from data.struct import Intrare
from data.struct import Produs

from utils import Error
from utils import Debug
from utils import Info

class DBFParser:
    
    FIELDS = list()

    def __init__(self, dbf_name):
        self._table = DBF(dbf_name)
        self._table_fields = self._table.field_names
        self._index_list = list()

        self._fields = list()
        self._records = list()
        self._record_objs = None

    def GetColumnIndex(self, key_list):
        index_list = [self._table_fields.index(_key) for _key in key_list]
        Debug("Key list {} produced index list: {}".format(key_list, index_list))
        return index_list

    def Populate(self, cls_type):
        if not self._index_list:
            Error("{}: index list is empty.".format(self.__class__))
            return

        self._fields = self.Extract(self._index_list, self._table_fields)
        if not self._fields:
            Error("{}: fields list empty.".format(self.__class__))
            return
        Info("Extracted fields: {}".format(self._fields))
        
        _records = list()
        for record in self._table:
            _records.append(self.Extract(self._index_list, list(record.values())))
        if not _records:
            Error("{}: records list empty.".format(self.__class__))
            return
        Info("Populated records: created {} entries.".format(len(_records)))

        # Create a list of cls_type objects.
        self._record_objs = dict() if cls_type == Intrare else list()
        for record in _records:
            if cls_type == Intrare:
                _object = cls_type(*record)
                id_intrare_key = record[0]
                date_key = record[4].strftime("%Y%m%d")
                self._record_objs[id_intrare_key] = _object
                # Adding object to date map entry. One date can have multiple entries.
                if date_key not in self._record_date_map:
                    self._record_date_map[date_key] = list()
                self._record_date_map[date_key].append(_object)
            else:
                self._record_objs.append(cls_type(*record))

    
    def Extract(self, index, input_list):
        return list(itemgetter(*index)(input_list))
    
    def GetRecordData(self):
        return self._record_objs
    
    def pprint(self):
        for record in self._record_objs:
            record.pprint()


class DBFParserIesiri(DBFParser):

    FIELDS = ["NR_IESIRE", "ID_IESIRE", "DENUMIRE", "DATA", "TOTAL", "NR_BONURI"]

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)

        self._index_list = self.GetColumnIndex(DBFParserIesiri.FIELDS)
        self.Populate(Iesire)


class DBFParserIntrari(DBFParser):

    FIELDS = ["ID_INTRARE", "NR_NIR", "NR_INTRARE", "DENUMIRE", "DATA", "TOTAL", "TIP"]

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)

        self._index_list = self.GetColumnIndex(DBFParserIntrari.FIELDS)
        self._record_date_map = dict()
        self.Populate(Intrare)
    
    def GetRecord(self, id_intrare):
        if id_intrare not in self._record_objs:
            Error("{}: Key {} not in record object list.".format(self.__class__, id_intrare))
            return
        return self._record_objs[id_intrare]
    
    def GetEntryFromDate(self, _date):
        return self._record_date_map[_date]
        
    def pprint(self):
        for key in self._record_objs:
            self._record_objs[key].pprint()



class DBFParserProduse(DBFParser):

    FIELDS = ["ID_U", "ID_INTRARE", "DENUMIRE", "DEN_GEST", "DEN_TIP", "TVA_ART", "CANTITATE", "PRET_VANZ"]

    def __init__(self, dbf_name):
        DBFParser.__init__(self, dbf_name)

        self._index_list = self.GetColumnIndex(DBFParserProduse.FIELDS)
        self.Populate(Produs)
    
