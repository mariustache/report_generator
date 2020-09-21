import wx
import pandas as pd

from data.parser import DBFParser
from data.parser import DBFParserIntrari
from data.parser import DBFParserIesiri
from data.parser import DBFParserProduse

from utils import NextDay


class ReportGenerator:

    INSTANCE = None

    def __init__(self):
        ReportGenerator.INSTANCE = self
        self._out_df_list = list()

    def GetDataFrameList(self):
        return self._out_df_list

    @classmethod
    def Instance(cls):
        return cls.INSTANCE


class JournalGenerator(ReportGenerator):

    COLUMNS = ["Data", "Documentul (felul, nr.)", "Felul operatiunii (explicatii)", "Incasari (numerar)", "Plati (numerar)", "Plati (alte)"]

    def __init__(self):
        ReportGenerator.__init__(self)
        JournalGenerator.INSTANCE = self
    
    def Generate(self, start_date, plati_numerar=0, plati_alte=0, incasari=0):
        current_date = start_date
        intrari_df = DBFParserIntrari.GetParser().GetDataWithDate(current_date)
        iesiri_df = DBFParserIesiri.GetParser().GetDataWithDate(current_date)

        while current_date <= pd.to_datetime(wx.DateTime.Now().Format("%Y%m%d")):
            _out_list = list()
            if not intrari_df.empty and not iesiri_df.empty:
                _out_list.append([current_date.strftime("%d-%m-%Y"), 0, "TOTAL PRECEDENT", incasari, plati_numerar, plati_alte])
                for index, row in intrari_df.iterrows():
                    if row["TIP"] == "C":
                        _out_list.append([row["DATA"].strftime("%d-%m-%Y"), row["NR_INTRARE"], "Alimentare {}".format(row["DENUMIRE"]), 0, 0, row["TOTAL"]])
                        plati_alte += row["TOTAL"]
                    else:
                        _out_list.append([row["DATA"].strftime("%d-%m-%Y"), row["NR_INTRARE"], "Cumparare marfa {}".format(row["DENUMIRE"]), 0, row["TOTAL"], 0])
                        plati_numerar += row["TOTAL"]
                for index, row in iesiri_df.iterrows():
                    _out_list.append([row["DATA"].strftime("%d-%m-%Y"), row["NR_IESIRE"], "Vanzare marfa {}".format(row["DENUMIRE"]), row["TOTAL"], 0, 0])
                    incasari += row["TOTAL"]
                
                _out_list.append([current_date.strftime("%d-%m-%Y"), 0, "TOTAL FINAL", incasari, plati_numerar, plati_alte])
            current_date = NextDay(current_date)
            intrari_df = DBFParserIntrari.GetParser().GetDataWithDate(current_date)
            iesiri_df = DBFParserIesiri.GetParser().GetDataWithDate(current_date)

            if _out_list:
                self._out_df_list.append(pd.DataFrame(_out_list, columns=self.COLUMNS))
        
        pd.set_option('display.expand_frame_repr', False)
        for _df in self._out_df_list:
            print(_df)
        
        writer = pd.ExcelWriter(r'D:\git\report_generator\data\jurnal_incasari_si_plati.xlsx')
        _start = 0
        for _df in self._out_df_list:
            _df.to_excel(writer, "Jurnal incasari si plati", startrow=_start)
            _start += len(_df) + 2
        writer.save()


class ManagementGenerator(ReportGenerator):
    
    COLUMNS = ["Numar document", "Explicatii", "Valoare lei (Marfuri)"]

    def __init__(self):
        ReportGenerator.__init__(self)
        ManagementGenerator.INSTANCE = self
    
    def Generate(self, start_date, sold_precedent=0):
        """
        Intrari, Iesiri and Produse are needed.
        Two tables.
        First table. 
            Columns: Numar document (NIR asociat), Explicatii, Valoare lei (marfuri);
            At the beginning of the table, print Sold precedent.
            At the end of the table, print Total intrari + sold (sum of all Intrari values and Sold precedent).

        Second table columns: 
            Columns: same
            At the end of the table, print Total vanzari + iesiri (end sum of first table minus the sum of all Iesiri values)
        """
        current_date = start_date
        intrari_df = DBFParserIntrari.GetParser().GetDataWithDate(current_date)
        iesiri_df = DBFParserIesiri.GetParser().GetDataWithDate(current_date)

        while current_date <= pd.to_datetime(wx.DateTime.Now().Format("%Y%m%d")):
            _out_list = list()
            if not intrari_df.empty and not iesiri_df.empty:
                _out_list.append(["Data: {}".format(current_date.strftime("%d-%m-%Y")), "Sold precedent", sold_precedent])
                
                _sum = 0
                for index, row in intrari_df.iterrows():
                    total_sum = self.GetProductSumFromId(row["ID_INTRARE"])
                    _out_list.append([row["NR_NIR"], "Cumparare marfa {}".format(row["DENUMIRE"]), total_sum])
                    _sum += total_sum
                sold_precedent += _sum
                
                _out_list.append(["", "Total intrari + sold", sold_precedent])
                _sum = 0
                for index, row in iesiri_df.iterrows():
                    _out_list.append([row["NR_IESIRE"], "Vanzare marfa {}".format(row["DENUMIRE"]), row["TOTAL"]])
                    _sum += row["TOTAL"]
                sold_final = sold_precedent - _sum
                
                _out_list.append(["", "Total vanzari + iesiri", sold_final])
                _out_list.append(["", "Sold final", sold_final])
                
                # Sold final for current date becomes sold precedent for the next date.
                sold_precedent = sold_final
                
            current_date = NextDay(current_date)
            intrari_df = DBFParserIntrari.GetParser().GetDataWithDate(current_date)
            iesiri_df = DBFParserIesiri.GetParser().GetDataWithDate(current_date)
        
            if _out_list:
                self._out_df_list.append(pd.DataFrame(_out_list, columns=self.COLUMNS))
        
        pd.set_option('display.expand_frame_repr', False)
        for _df in self._out_df_list:
            print(_df)
            
        writer = pd.ExcelWriter(r'D:\git\report_generator\data\raport_de_gestiune.xlsx')
        _start = 0
        for _df in self._out_df_list:
            _df.to_excel(writer, "Raport de gestiune", startrow=_start)
            _start += len(_df) + 2
        writer.save()
    
    def GetProductSumFromId(self, id_intrare):
        produse_df = DBFParserProduse.GetParser().GetDataWithIdIntrare(id_intrare)
        return produse_df.apply(lambda row: row["CANTITATE"] * row["PRET_VANZ"], axis='columns').sum()
