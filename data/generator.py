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

    @classmethod
    def Instance(cls):
        return cls.INSTANCE


class JournalGenerator(ReportGenerator):

    COLUMNS = ["Data", "Documentul (felul, nr.)", "Felul operatiunii (explicatii)", "Incasari (numerar)", "Plati (numerar)", "Plati (alte)"]

    def __init__(self):
        ReportGenerator.__init__(self)
        JournalGenerator.INSTANCE = self
        # Set initial values
        # TODO: get values from config file or from user input. TBD
        self._output_list = [["", "", "", 0, 0, 0]]
        #self._output_df = pd.DataFrame([series], columns=self.COLUMNS)
    
    def Generate(self, start_date):
        intrari_df = DBFParserIntrari.GetParser().GetDataWithDate(start_date)
        iesiri_df = DBFParserIesiri.GetParser().GetDataWithDate(start_date)

        current_date = start_date
        while not intrari_df.empty or not iesiri_df.empty:

            for index, row in intrari_df.iterrows():
                self._output_list.append([row["DATA"].strftime("%d-%m-%Y"), row["NR_INTRARE"], "Cumparare marfa {}".format(row["DENUMIRE"]), 0, row["TOTAL"], 0])
            for index, row in iesiri_df.iterrows():
                self._output_list.append([row["DATA"].strftime("%d-%m-%Y"), row["NR_IESIRE"], "Vanzare marfa {}".format(row["DENUMIRE"]), row["TOTAL"], 0, 0])
            
            current_date = NextDay(current_date)
            intrari_df = DBFParserIntrari.GetParser().GetDataWithDate(current_date)
            iesiri_df = DBFParserIesiri.GetParser().GetDataWithDate(current_date)
        
        self._output_df = pd.DataFrame(self._output_list, columns=self.COLUMNS)
        pd.set_option('display.expand_frame_repr', False)
        print(self._output_df)


class ManagementGenerator(ReportGenerator):

    def __init__(self):
        ReportGenerator.__init__(self)
        ManagementGenerator.INSTANCE = self
    
    def Generate(self, start_date):
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
        pass