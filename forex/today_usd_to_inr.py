from datetime import datetime, timedelta
import urllib2
import json
from bs4 import BeautifulSoup

def get_usd_to_inr_for_today():
    url = r'http://free.currencyconverterapi.com/api/v3/convert?q=USD_INR&compact=ultra'
    usd_to_inr = json.loads(urllib2.urlopen(url).read())

    return usd_to_inr['USD_INR']


def get_usd_to_inr_for_date(date):
    url = r'https://www.x-rates.com/historical/?from=INR&amount=1&date={}'.format(date)
    page = BeautifulSoup(urllib2.urlopen(url), "html.parser")

    tag_list = [sub_section.findAll('a') for sub_section in page.findAll('td', {"class":"rtRates"})]
    #Remove duplicates
    tag_list = tag_list
    lines = [line[0] for line in tag_list]

    for line in lines:
        ln = str(line)
        if 'to=INR' in ln  and 'from=USD' in ln :
            extract_dollar_to_inr = ln .split('>')[1].split('<')[0]
            return float(extract_dollar_to_inr)


def usd_to_inr_for_date(_date=None):
    # try for 3 back date
    _date = datetime.now().strftime("%Y-%m-%d") if not _date else _date.strftime("%Y-%m-%d")
    max_back_date = 3
    for minus_date in range(0, max_back_date):
        price = get_usd_to_inr_for_date(_date)
        if not price:
            _date = (datetime.strptime(_date,"%Y-%m-%d") - timedelta(days=minus_date)).strftime("%Y-%m-%d")
            get_usd_to_inr_for_date(_date)
        if price:
            return price
    else:
        print("Error: Something wrong with finding  usd to inr, may be date format is wrong")


if __name__ == '__main__':
    print usd_to_inr_for_date()