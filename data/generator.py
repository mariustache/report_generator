
from data.parser import DBFParser
from data.parser import DBFParserIntrari
from data.parser import DBFParserIesiri
from data.parser import DBFParserProduse

from pandas import DataFrame


class ReportGenerator:

    INSTANCE = None

    def __init__(self):
        ReportGenerator.INSTANCE = self
    
    def GenerateJournal(self, start_date):
        pass
    
    def GenerateManagementReport(self, start_date):
        pass
    
    @classmethod
    def Instance(cls):
        return cls.INSTANCE