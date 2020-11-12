# Generate dataframes of the stock data within the timeframe specified


import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import pickle
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

def save_sp500_tickers():
    list_tags = []

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    html = urllib.request.urlopen(url,context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('table',) #('table', {'class':wikitable soratble})
    #this should help if there are multiple tables on the wikipage

    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker =row.findAll('td')[0]
        tickers.append(ticker)
#this for loop was supposed to pull the tickers from the 1st column ('td'[0])
# but this did not work for me so I modified lines 12 to 21 and added the for
# loop below that takes the output from the above for and slice out the tickers

    for thing in tickers:
        tic_tag = re.findall(".*nofollow\"\>(.*)\<", str(thing))
        list_tags.append(tic_tag[0])


    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(list_tags, f)

    print(list_tags)
    return list_tags

#wb = write bytes
#pickle.dump('dump what', 'as what')
#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
        #when calling the function if we type the argument as True then we will
        # recall the save_sp500_tickers function else we will pull the pickle file
        # we created. This will be useful when we want to run an update on the
        #tickers
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tickers:
        print(ticker)
        try:
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                df = web.DataReader(ticker,'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                print('Already have{}'.format(ticker))
        except:
            continue

#get_data_from_yahoo()
