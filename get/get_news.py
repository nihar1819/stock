import csv
import time
import requests
from bs4 import BeautifulSoup
#from pattern.en import ngrams
import urllib2
from get import stock_list
import constants


def get_news_link(list_of_stock):
    """This function build news link and return it.

    :param dict list_of_stock: stock full name and symbol
    :return: list of dictinary [{stock_name:url.html}, ...]
    """

    # Create a list of the news section urls of the respective companies
    url_list = [{k:'{}/company-article/{}/news/{}#{}'.format(constants.BASE_URL, k, v, v)} for k, v in
                list_of_stock.iteritems()]
    return url_list


def get_news_urls_for_single_stock(stock_name, url):
    """Return list of news url for a given stock base news url

    :param stock_name:
    :param url:
    :return:
    """
    response = urllib2.urlopen(url)
    webcontent = response.read()

    soup = BeautifulSoup(webcontent,"html.parser")
    urls = list()

    for url in soup.find_all('a'):
        try:
            partial_url = url.get('href')
            if str(partial_url).startswith('/news') and stock_name in str(partial_url):
                url = "{}{}".format(constants.BASE_URL,partial_url)
                urls.append(url)
        except Exception as e:
            print e.message
            continue
    return list(set(urls))


def get_news_urls_for_all_stocks():
    # list of stock is a dictionary eg: {'cadilahealthcare': 'CHC', 'piramalenterprises': 'PH05' }
    list_of_stock = stock_list.get_stock_list()

    stocks_news_base_urls = get_news_link(list_of_stock)

    output = dict()
    for stock_news_url in stocks_news_base_urls:
        stock = stock_news_url.keys()[0]
        news_url = stock_news_url[stock]
        print
        output[stock] = dict(news_urls=get_news_urls_for_single_stock(stock, news_url))

    return output


def get_news_content(url):
    """Provide all the content in the form of list of word present in the url

    :param url:
    :return:
    """
    pass


def get_news_for_a_stock_from_all_url(stock_name, news_urls):
    for news_url in news_urls:
        data = get_news_content(news_url)
        print data
        break

data = get_news_urls_for_all_stocks()
for stock_name, news_urls in data.iteritems():
    get_news_for_a_stock_from_all_url(stock_name, news_urls['news_urls'])






