from urllib2 import Request
import urllib2
import re

HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                     '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}


def get_stock_price(stock_symbol):
    url_sample = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}&illiquid=0&smeFlag=0&itpFlag=0'
    url = url_sample.format(stock_symbol)
    req = Request(url, headers=HDR)
    page = urllib2.urlopen(req)
    data = page.read()
    search = '"lastPrice":"(.+?)"'
    re_pattern = re.compile(search)
    return re.findall(re_pattern, data)


def get_live_prices(stock_symbol_list=[]):
    print [get_stock_price(stock_symbol) for stock_symbol in stock_symbol_list]


get_live_prices(['SBIN', 'BHAGYANGR'])