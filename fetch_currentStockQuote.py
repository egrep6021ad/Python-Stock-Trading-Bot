import requests
from datetime import datetime
import csv
from datetime import date

today = date.today()
today = str(today)

def getQuotes(tickers,td_consumer_key):
  quotes_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
  # Data needed:
  data_dictionary = {}
  # Data points:
  fields = ['description',
            'Open Price',
            'Bid Price',
            'Ask Price',
            'Net % Change (decimal)',
            'Market % change (decimal)']
  # Fetch each ticker's quote:
  for stock in tickers:
    endpoint = quotes_url.format(stock_ticker = stock)
    quotes = requests.get(url=endpoint, 
              params={'apikey' : td_consumer_key})
    # Jsonify()
    data = quotes.json()
    # Build Dictionary   
    temp = (data[stock]['description'],
            data[stock]['openPrice'],
            data[stock]['bidPrice'],
            data[stock]['askPrice'],
            data[stock]['netPercentChangeInDouble'],
            data[stock]['markPercentChangeInDouble'])
    data_dictionary.update({data[stock]['description']:temp})
    
  # Dictionary -> CSV
  with open(f'./{today}/{today[5:]}\'s_quotes.csv', 'w+') as f: 
    writer = csv.writer(f)
    writer.writerow(fields)
    for x in data_dictionary:
      writer.writerow(data_dictionary[x])
  return 0

