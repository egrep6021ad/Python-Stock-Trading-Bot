# Main little tutorial:
# https://medium.com/analytics-vidhya/an-introduction-to-the-td-ameritrade-api-in-python-8c9d462e966c

# Working with JSON / Python:
# https://realpython.com/python-json/

# Prints JSON nicely:
from pprint import pprint
#import json
from datetime import datetime
import time
import os
import requests
import csv
from datetime import date
today = date.today()
today = str(today)

path = f"./{today}"
exist = os.path.exists(path)
if not exist:
  os.makedirs(path)

my_secret = os.environ['POOP']
td_consumer_key =my_secret


quotes_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
base = "https://api.tdameritrade.com/v1/accounts/{account}"
movers_url = "https://api.tdameritrade.com/v1/marketdata/{index}/movers"
fundamentals_url = 'https://api.tdameritrade.com/v1/instruments?&symbol={stock_ticker}&projection={projection}'
options_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={date}&toDate={date}'


def get_biggest_daily_movers():
  big_movers = {}
  movers_symbols = []
  fields = ['Desciption',
            'Symbol',
            'Direction',
            'Change ( % )']
  
  indexes = ['$DJI','$SPX.X','$COMPX']
  for i in indexes:
  # Fetch data
    endpoint = movers_url.format(index = i)
    data = requests.get(url=endpoint, 
                params={'apikey' : td_consumer_key})
    # Jsonify()
    data = data.json()
    # Parse JSON -> Dictionary 
    for x in data:
      change = x['change'] * 100
      temp = (x['description'],
              x['symbol'],
              x['direction'],
              f'{change :0.3f}')
      
      movers_symbols.append(x['symbol'])
      big_movers.update({movers_symbols[-1] : temp})
    # Dictionary -> CSV
  with open(f'./{today}/{today[5:]}\'s big moves.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(fields)
    for x in big_movers:
      writer.writerow(big_movers[x])
  return movers_symbols


def get_quotes(tickers):
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
  with open(f'./{today}/{today[5:]}\'s_quotes.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(fields)
    for x in data_dictionary:
      writer.writerow(data_dictionary[x])
  return 0

def get_fundamentals(ticker):
  fundamentals_dict = {}
  # Data points:
  fields = ['description',
            'Exchange',
            'Earnings Per Share (Growth %)',
            'Beta',
            'P/E Ratio',
            'High-52',
            'Low-52',
            'Market Cap',
            'Market Cap Float',
            'Dividend Pay: ',
            'Dividend Pay Date:',
            'Net Profit Margin (TTM)']
  # Fetch data:
  
  for x in ticker:
    try:
      endpoint = fundamentals_url.format(stock_ticker = x,
          projection = 'fundamental')
      fundamentals = requests.get(url=endpoint, 
                  params={'apikey' : td_consumer_key})
      # Jsonify()
   
      data = fundamentals.json()
      # Json -> Dictionary
      temp = (data[x]['description'],
              data[x]['exchange'],
              data[x]['fundamental']['epsChangeYear'],
              data[x]['fundamental']['beta'],
              data[x]['fundamental']['peRatio'],
              data[x]['fundamental']['high52'],
              data[x]['fundamental']['low52'],
              data[x]['fundamental']['marketCap'],
              data[x]['fundamental']['marketCapFloat'],
              data[x]['fundamental']['dividendPayAmount'],
              data[x]['fundamental']['dividendPayDate'],
              data[x]['fundamental']['netProfitMarginTTM'])
      
      fundamentals_dict.update({data[x]['description']: temp})
    except KeyError:
      print("KEY ERROR:")
      continue
  print(fundamentals)
 # Dictionary -> CSV
  with open(f'./{today}/{today[5:]}\'s fundamentals.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(fields)
    for x in fundamentals_dict:
      writer.writerow(fundamentals_dict[x])
  return 0



def get_history(ticker):
  endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
 
  candleStick_dict = {}
  fields = ['Day','Open', 'Close', 'High', 'Low', 'Volume']
  num = 0
  for i in ticker:
    full_url = endpoint.format(stock_ticker=i,periodType='month',period=3,frequencyType='daily',frequency=1)
    page = requests.get(url=full_url,
                        params={'apikey' : td_consumer_key})
    #content = json.loads(page.content)
    data = page.json()
    temp = data['candles']

    for x in temp:
      z = (  num,
           x['open'],
           x['close']
           ,x['high']
           ,x['low'],
           x['volume'] )
      candleStick_dict.update({num : z})
      num += 1
    
  with open(f'./{today}/{today[5:]}\'s candle_stick.csv', 'w') as f: 
    writer = csv.writer(f)
    f.write(f'ticker: {ticker}\n')
    writer.writerow(fields)
    for x in candleStick_dict:
      writer.writerow(candleStick_dict[x])
  return 0  




#Options arent working!
def options():
  ts =00
  datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  print('options:')
  base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={date}&toDate={date2}'
  endpoint = base_url.format(stock_ticker = 'AAL',
    contractType = 'PUT',
    date='2022-05-10',date2='2022-05-17')
  data = requests.get(url=endpoint, 
              params={'apikey' : td_consumer_key})
  
  #content = json.loads(page.content)
  data = data.json()
  pprint(data)
  print(type(data))
  



if __name__ == "__main__":
  # Returns array of SYMBOLS for days biggest movers:
  #arr = get_biggest_daily_movers()
  #time.sleep(5)
  #print("40 Seconds.")
  # Get Quotes for all of those big movers:
  #get_quotes(arr)
  #time.sleep(20)
  print("30 Seconds..")
  # Get fundamentals on the biggest movers:
  #get_fundamentals(arr)
  #time.sleep(20)
  print("20 Seconds...")
  get_history(['$DJI'])
  print(f'Done! check {today}\'s folder!')
  #options()

