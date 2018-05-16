from urllib2 import Request, URLError, HTTPError
import urllib2
import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
import os
import urllib2,cookielib

yesterday = (date.today() - timedelta(1)).strftime('%d%m%Y')
VOLATILITY_FILE_NAME = "CMVOLT_{}.CSV".format(yesterday)
VOLATILITY_FILE_PATH = r"./{}".format(VOLATILITY_FILE_NAME)

volatility_url = r'https://www.nseindia.com/archives/nsccl/volt/{}'.format(VOLATILITY_FILE_NAME)

nifty_100_url = r'https://www.nseindia.com/content/indices/ind_nifty100list.csv'
nifty_100_file_name = nifty_100_url.split('/')[-1]
NIFTY_100_FILE_PATH = r"./{}".format(nifty_100_file_name)

#site= "http://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=JPASSOCIAT&fromDate=1-JAN-2012&toDate=1-AUG-2012&datePeriod=unselected&hiddDwnld=true"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def download_file(url, output_file_path, check_file_presence=False):
    need_to_download = True
    if check_file_presence and os.path.exists(output_file_path):
        need_to_download = False

    if need_to_download:
        try:
            req = Request(url, headers=hdr)
            f = urllib2.urlopen(req)

            local_file = open(output_file_path, "wb")
            local_file.write(f.read())
            local_file.close()
        except HTTPError, e:
            print "HTTP Error:", e.code, url
        except URLError, e:
            print "URL Error:", e.reason, url


def get_csv():
    download_file(volatility_url, VOLATILITY_FILE_NAME, True)
    download_file(nifty_100_url, NIFTY_100_FILE_PATH, True)


def cleanup():
    try:
        os.remove(VOLATILITY_FILE_PATH)
    except Exception as e:
        print "Error: Delete Failed: {} file not found".format(VOLATILITY_FILE_NAME)
        print e.message


def get_daily_volatility_partial():
    full_df = pd.read_csv(VOLATILITY_FILE_PATH)
    full_df.rename(columns={"Current Day Underlying Daily Volatility (E) = Sqrt(0.94*D*D + 0.06*C*C)": "daily",
                            "Underlying Annualised Volatility (F) = E*Sqrt(365)": "yearly"}, inplace=True)

    df = full_df[['Symbol', 'daily', 'yearly']]
    df['daily_percent%'] = df['daily'] * 100
    df['yearly %'] = df[['yearly']] * 100
    return df


def combine_daily_volatility_and_nifty100():
    volatility_df = get_daily_volatility_partial()
    nifty_100_df = pd.read_csv(NIFTY_100_FILE_PATH)
    merged_df = volatility_df.loc[volatility_df['Symbol'].isin(nifty_100_df['Symbol'])]

    merged_df = pd.merge(merged_df,nifty_100_df, on='Symbol')
    final_merged_df = merged_df[['Company Name', 'Symbol', 'daily_percent%', 'yearly %', 'Industry']]
    return final_merged_df


def get_daily_volatity():
    import numpy as np
    df = combine_daily_volatility_and_nifty100()
    df = df.sort_values(['daily_percent%'],ascending=[0])
    print df[['Symbol', 'daily_percent%', 'yearly %']][df['daily_percent%']>1.90]


def main():
    get_daily_volatity()


if __name__ == '__main__':
    print "hello"
    main()

