# https://medium.com/analytics-vidhya/an-introduction-to-the-td-ameritrade-api-in-python-8c9d462e966c
import os
import requests
#import json
from pprint import pprint
my_secret = os.environ['POOP']
td_consumer_key =my_secret

quotes_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
history_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory'
base = "https://api.tdameritrade.com/v1/accounts/{account}"
movers_url = "https://api.tdameritrade.com/v1/marketdata/{index}/movers"
fundamentals_url = 'https://api.tdameritrade.com/v1/instruments?&symbol={stock_ticker}&projection={projection}'
options_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={date}&toDate={date}'



print("movers:")
endpoint = movers_url.format(index = '$DJI')
movers = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
#pprint(movers.json())

print("History:")
endpoint = history_url.format(stock_ticker = 'AAL')
history = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
#pprint(history.json())

print("Quotes:")
endpoint = quotes_url.format(stock_ticker = 'TSLA')
quotes = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
pprint(quotes.json())

print("fundamentals:")
endpoint = fundamentals_url.format(stock_ticker = 'TSLA',
    projection = 'fundamental')
fundamentals = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
pprint(fundamentals.json())

#Options arent working!
print('options:')
endpoint = options_url.format(stock_ticker = 'CNNE',
    contractType = 'PUT',
    date='2022-04-09')
options = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
#pprint(options.json())


