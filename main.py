# Main little tutorial:
# https://medium.com/analytics-vidhya/an-introduction-to-the-td-ameritrade-api-in-python-8c9d462e966c

# Working with JSON / Python:
# https://realpython.com/python-json/

# Prints JSON nicely:
# from pprint import pprint

import os
import requests
import json
import csv
from datetime import date

my_secret = os.environ['POOP']
td_consumer_key =my_secret

quotes_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
history_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory'
base = "https://api.tdameritrade.com/v1/accounts/{account}"
movers_url = "https://api.tdameritrade.com/v1/marketdata/{index}/movers"
fundamentals_url = 'https://api.tdameritrade.com/v1/instruments?&symbol={stock_ticker}&projection={projection}'
options_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={date}&toDate={date}'



#print("movers:")
#endpoint = movers_url.format(index = '$DJI')
#movers = requests.get(url=endpoint, 
#            params={'apikey' : td_consumer_key})
#pprint(movers.json())
#
#print("History:")
#endpoint = history_url.format(stock_ticker = 'AAL')
#history = requests.get(url=endpoint, 
#           params={'apikey' : td_consumer_key})
#pprint(history.json())

print("Quotes:")
# Data needed:
today = date.today()
today = str(today)
data_dictionary = {}
daily_data = ['TSLA','AAPL','NFLX']
fields = ['description','openPrice',
           'bidPrice','askPrice',
           'netPercentChangeInDouble','markPercentChangeInDouble']  

for tickers in daily_data:
  endpoint = quotes_url.format(stock_ticker = tickers)
  quotes = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
  # Jsonify()
  data = quotes.json()
  # Append to json file
  #with open("data_file.json", "a+") as write_file:
   # json.dump(data, write_file)
  # Build Dictionary   
  temp = (data[tickers]['description'],data[tickers]['openPrice'],data[tickers]['bidPrice'],data[tickers]['askPrice'],data[tickers]['netPercentChangeInDouble'],data[tickers]['markPercentChangeInDouble'])
  data_dictionary.update({data[tickers]['description']:temp})

# Dictionary -> CSV
with open(f'{today[5:]}.csv', 'a+') as f: 
  writer = csv.writer(f)
  writer.writerow(fields)
  for x in data_dictionary:
    writer.writerow(data_dictionary[x])




#print("fundamentals:")
#endpoint = fundamentals_url.format(stock_ticker = 'TSLA',
#    projection = 'fundamental')
#fundamentals = requests.get(url=endpoint, 
#            params={'apikey' : td_consumer_key})
#pprint(fundamentals.json())

#Options arent working!
#print('options:')
#endpoint = options_url.format(stock_ticker = 'CNNE',
#    contractType = 'PUT',
#    date='2022-04-09')
#options = requests.get(url=endpoint, 
#            params={'apikey' : td_consumer_key})
#pprint(options.json())


