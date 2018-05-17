import csv
import pandas as pd
import urllib
import os

data = 'data/'
archive = 'archive/'


def download():
    granularities = [
        ('d', 'day'),
        ('w', 'week'),
        ('m', 'month'),
        ('a', 'year')
    ]
    source = 'https://www.eia.gov/dnav/pet/hist_xls/RBRTE'
    for a in granularities:
        urllib.urlretrieve(
            source + a[0] + '.xls',
            archive + 'brent-' + a[1] + '.xls')

    source = 'http://www.eia.gov/dnav/pet/hist_xls/RWTC'
    for a in granularities:
        urllib.urlretrieve(
            source + a[0] + '.xls',
            archive + 'wti-' + a[1] + '.xls')


def process():
    for dirs, subdirs, files in os.walk(archive):
        for file in files:
            df = pd.read_excel(os.path.join(dirs, file), sheetname=1)
            df = df.iloc[2:]
            format_str = '%d-%m-%Y'
            if 'year' in file:
                format_str = '%Y'
            if 'month' in file:
                format_str = "%m-Y"
            df['date'] = df['date'].dt.strftime(format_str)
            name = data + file.split('.xls')[0] + '.csv'
            df.to_csv(open(name, 'w+'), sep=",", index=False)


if __name__ == '__main__':
    download()
    process()
