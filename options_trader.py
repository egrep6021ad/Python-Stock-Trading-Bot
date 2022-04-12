import csv
from datetime import date
from collections import OrderedDict
import os
from pprint import pprint


# Variable
path = "Quick"
exist = os.path.exists(path)
if not exist:
  os.makedirs(path)
# Variable
today = date.today() 
today = str(today)



def import_from_csv(type):
  with open(f'./{today}/{today[5:]}\'s {type}_options.csv', mode='r') as f:
      options = {}
      reader = csv.reader(f)
      n = 0
      for row in reader:
        description = row[0]
        ticker = row[1]
        strike = row[2]
        in_money = row[3]
        stock_ask = row[4]
        stock_bid = row[5]
        option_ask = row[6]
        option_bid = row[7]
        theoretical_val = row[8]
        delta = row[9]
        gamma = row[10]
        theta = row[11]
        vega = row[12]
        time_val = row[13]
        volatility = row[14]
        theoretical_volitility = row[15]
        quoteDate = row[16]
        trade_time = row[17]

        options.update({n : (description, ticker, strike,in_money,stock_ask,stock_bid,option_ask,option_bid,theoretical_val,delta,gamma,theta,vega,time_val,volatility,theoretical_volitility,quoteDate,trade_time)})
        n += 1
  return options

def data_handler(options):
   with open(f'./Quick/{today[5:]} options.txt', 'w+') as fp:
    for (k,v) in options.items():
      fp.write(f"{v[0]}\n")
      fp.write(f"SYM: {v[1]}\n")
      fp.write(f"Strike: {v[2]}\n")
      fp.write(f"Stock Ask: {v[4]}\n")
      fp.write(f"Stock Bid: {v[5]}\n")
      fp.write(f"IN the Money: {v[3]}\n")
      fp.write(f"Option Ask: {v[6]}\n")
      fp.write(f"Option Bid: {v[7]}\n")
      fp.write(f"Theoretical Value: {v[8]}\n")
      fp.write(f"Delta: {v[9]}\n")
      fp.write(f"Gamma: {v[10]}\n")
      fp.write(f"Theta: {v[11]}\n")
      fp.write(f"Vega: {v[12]}\n")
      fp.write(f"Time Val: {v[13]}\n")
      fp.write(f"Volatility: {v[14]}\n")
      fp.write(f"Thoeoretical Volatility: {v[15]}\n")
      fp.write(f"Quote Date: {v[16]}\n")
      fp.write(f"Expiration Date: {v[17]}\n\n")
      
  


  
if __name__ == "__main__":
  dict = import_from_csv("CALL")
  data_handler(dict)
  dict = import_from_csv("PUT")
