import requests
import csv
from datetime import date

today = date.today()
today = str(today)


def getMovers(td_consumer_key, direction):
  movers_url = "https://api.tdameritrade.com/v1/marketdata/{index}/movers"

  
  big_movers = {}
  movers_symbols = []
  fields = ['Desciption',
            'Symbol',
            'Direction',
            'Change ( % )',
             'Total Volume']
  
  indexes = ['$DJI','$SPX.X','$COMPX']
  for i in indexes:
  # Fetch data
    endpoint = movers_url.format(index = i)
    data = requests.get(url= endpoint, 
                params={'apikey' : td_consumer_key,
                       'direction' : direction})
  
    # Jsonify()
    data = data.json()
    
    # Parse JSON -> Dictionary 
    for x in data:
      change = x['change'] * 100
      temp = (x['description'],
              x['symbol'],
              x['direction'],
              f'{change :0.3f}',
              x['totalVolume'])
      
      movers_symbols.append([
        x['description'],
        x['direction'],
        x['change'],
        x['totalVolume'],
        x['symbol']
      ])
      big_movers.update({movers_symbols[-1][-1] : temp})
    # Dictionary -> CSV
  with open(f'./{today}/{today[5:]}\'s big moves.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(fields)
    for x in big_movers:
      writer.writerow(big_movers[x])
  return movers_symbols




