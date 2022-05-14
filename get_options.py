import requests
from datetime import datetime
import csv
from datetime import date

today = date.today()
today = str(today)

def getOptions(stock,td_consumer_key):
  quotes_url = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
  # Get underlying Stock information:
  endpoint = quotes_url.format(stock_ticker = stock)
  quotes = requests.get(url=endpoint, 
              params={'apikey' : td_consumer_key})
  data = quotes.json()
  
   # Build Dictionary   
  temp = (data[stock]['description'],
          data[stock]['openPrice'],
          data[stock]['bidPrice'],
          data[stock]['askPrice'],
          data[stock]['netPercentChangeInDouble'],
          data[stock]['markPercentChangeInDouble'])
  

  base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={date}&toDate={date2}&range={range}'
  
  endpoint = base_url.format(stock_ticker = stock,
    contractType = 'ALL',
    date='2022-04-12',date2='2022-06-17',range='NTM')
  data = requests.get(url=endpoint, 
              params={'apikey' : td_consumer_key})
  

  data = data.json()
  with open(f'./{today}/{today[5:]}\'s PUT_options.csv', 'w+') as f: 
    dict = {}
    n = 0
    pen = csv.writer(f)
    k = data['putExpDateMap']
    for (key,value) in k.items():
      for (k,v) in value.items():
        quoteDate = datetime.utcfromtimestamp((v[0]['quoteTimeInLong']/1000)).strftime('%Y-%m-%d %H:%M:%S')
        trade_time = datetime.utcfromtimestamp((v[0]['expirationDate']/1000)).strftime('%Y-%m-%d %H:%M:%S')
  
  
        option_info = (v[0]['description'],temp[0],v[0]['strikePrice'],v[0]['inTheMoney'],temp[2],temp[3],v[0]['ask'],v[0]['bid'],v[0]['theoreticalOptionValue'],v[0]['delta'],v[0]['gamma'],v[0]['theta'],v[0]['vega'],v[0]['timeValue'],v[0]['volatility'],v[0]['theoreticalVolatility'],quoteDate,trade_time)
        dict.update({n : option_info})
        n += 1
    for x in dict:
      pen.writerow(dict[x])
    dict = {}
    n = 0
    
  with open(f'./{today}/{today[5:]}\'s CALL_options.csv', 'w+') as f: 
    pen = csv.writer(f)
    k = data['callExpDateMap']
    for (key,value) in k.items():
      for (k,v) in value.items():
        quoteDate = datetime.utcfromtimestamp((v[0]['quoteTimeInLong']/1000)).strftime('%Y-%m-%d %H:%M:%S')
        trade_time = datetime.utcfromtimestamp((v[0]['expirationDate']/1000)).strftime('%Y-%m-%d %H:%M:%S')
  
  
        option_info = (v[0]['description'],temp[0],v[0]['strikePrice'],v[0]['inTheMoney'],temp[2],temp[3],v[0]['ask'],v[0]['bid'],v[0]['theoreticalOptionValue'],v[0]['delta'],v[0]['gamma'],v[0]['theta'],v[0]['vega'],v[0]['timeValue'],v[0]['volatility'],v[0]['theoreticalVolatility'],quoteDate,trade_time)
        dict.update({n : option_info})
        n += 1
    for x in dict:
      pen.writerow(dict[x])
      
  return  0
    


    
    
    
  



