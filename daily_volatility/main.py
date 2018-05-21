import os

import pandas as pd

import get_csv


#site= "http://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=JPASSOCIAT&fromDate=1-JAN-2012&toDate=1-AUG-2012&datePeriod=unselected&hiddDwnld=true"


def cleanup():
    try:
        os.remove(get_csv.VOLATILITY_FILE_PATH)
    except Exception as e:
        print "Error: Delete Failed: {} file not found".format(get_csv.VOLATILITY_FILE_NAME)
        print e.message


def get_daily_volatility_partial():
    full_df = pd.read_csv(get_csv.VOLATILITY_FILE_PATH)
    full_df.rename(columns={"Current Day Underlying Daily Volatility (E) = Sqrt(0.94*D*D + 0.06*C*C)": "daily",
                            "Underlying Annualised Volatility (F) = E*Sqrt(365)": "yearly"}, inplace=True)

    df = full_df[['Symbol', 'daily', 'yearly']]
    df['daily_percent%'] = df['daily'] * 100
    df['yearly %'] = df[['yearly']] * 100
    return df


def combine_daily_volatility_and_nifty100():
    volatility_df = get_daily_volatility_partial()
    nifty_100_df = pd.read_csv(get_csv.NIFTY_100_FILE_PATH)
    merged_df = volatility_df.loc[volatility_df['Symbol'].isin(nifty_100_df['Symbol'])]

    merged_df = pd.merge(merged_df,nifty_100_df, on='Symbol')
    final_merged_df = merged_df[['Company Name', 'Symbol', 'daily_percent%', 'yearly %', 'Industry']]
    return final_merged_df


def get_daily_volatity():
    df = combine_daily_volatility_and_nifty100()
    df = df.sort_values(['daily_percent%'],ascending=[0])
    print df[['Symbol', 'daily_percent%', 'yearly %']][df['daily_percent%']>1.90]


def main():
    get_csv.get_csv()
    get_daily_volatity()


if __name__ == '__main__':
    main()
