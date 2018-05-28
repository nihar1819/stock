import intraday
import csv
import pandas as pd
from os import path
import download_all_equity_list
from daily_volatility import main

def read_file():
    if not path.exists(intraday.ALL_EQUITY_FILE_PATH):
        download_all_equity_list.download_all_equity()

    pd.DataFrame.from_csv(intraday.ALL_EQUITY_FILE_PATH)
    print main.get()

read_file()