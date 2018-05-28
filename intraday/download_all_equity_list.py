from urllib2 import Request
import urllib2
import csv
import intraday


def download_all_equity():
    req = Request(intraday.URD_ALL_NSE_STOCK_LIST,headers=intraday.HDR)
    cr = csv.reader(urllib2.urlopen(req))

    with open(intraday.ALL_EQUITY_FILE_PATH, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        [writer.writerow(line) for line in cr]
