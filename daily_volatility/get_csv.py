from urllib2 import Request, URLError, HTTPError
import urllib2
from datetime import date
from datetime import datetime
from datetime import timedelta
import os


def get_yesterday_str(format='%d_%m_%Y'):
    if datetime.now().weekday() == 0 and (datetime.now().time().hour < 15 and datetime.now().minute < 30):
        date_str = (date.today() - timedelta(3)).strftime(format)
    elif (datetime.now().time().hour == 15 and datetime.now().minute > 30) or datetime.now().time().hour > 15:
        date_str = (date.today()).strftime(format)
    else:
        date_str = (date.today() - timedelta(1)).strftime(format)

    return date_str


VOLATILITY_FILE_NAME = "CMVOLT_{}.CSV".format(get_yesterday_str('%d%m%Y'))
VOLATILITY_FILE_PATH = r"./resources/{}".format(VOLATILITY_FILE_NAME)

volatility_url = r'https://www.nseindia.com/archives/nsccl/volt/{}'.format(VOLATILITY_FILE_NAME)

nifty_100_url = r'https://www.nseindia.com/content/indices/ind_nifty100list.csv'
nifty_100_file_name = nifty_100_url.split('/')[-1]
NIFTY_100_FILE_PATH = r"./resources/{}".format(nifty_100_file_name)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def get_deliverable_file_path():
    date_str = get_yesterday_str()

    file_name = "{}_{}.csv".format(date_str,'deleverables')
    file_path = r'./resources/{}'.format(file_name)
    return file_path


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
    download_file(volatility_url, VOLATILITY_FILE_PATH, True)
    download_file(nifty_100_url, NIFTY_100_FILE_PATH, True)

    deliverable_url = r'https://www.nseindia.com/products/content/sec_bhavdata_full.csv'
    download_file(deliverable_url, get_deliverable_file_path())

if __name__ == '__main__':
    get_deliverable_file_path()