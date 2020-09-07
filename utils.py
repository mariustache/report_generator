
import pandas as pd


def Error(message):
    print("[ERROR] {}".format(message))
    
def Info(message):
    print("[INFO] {}".format(message))

def Debug(message):
    print("[DEBUG] {}".format(message))

def NextDay(current_date):
    return current_date + pd.to_timedelta(1, unit='d')
