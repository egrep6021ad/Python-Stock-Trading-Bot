import requests
from datetime import datetime
import csv
from datetime import date

today = date.today()
today = str(today)


def getFundamentals(ticker,td_consumer_key):
  fundamentals_url = 'https://api.tdameritrade.com/v1/instruments?&symbol={stock_ticker}&projection={projection}'
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
 
 # Dictionary -> CSV
  with open(f'./{today}/{today[5:]}\'s fundamentals.csv', 'w') as f: 
    writer = csv.writer(f)
    writer.writerow(fields)
    for x in fundamentals_dict:
      writer.writerow(fundamentals_dict[x])
  return 0