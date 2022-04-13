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
# Import Data from CSV
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
        n += 1
        options.update({n : (description, ticker, strike,in_money,stock_ask,stock_bid,option_ask,option_bid,theoretical_val,delta,gamma,theta,vega,time_val,volatility,theoretical_volitility,quoteDate,trade_time)})
  return options
# Write to TXT File
def data_handler(options,r):
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
      
    print(f"\nOptions Analysis: {v[0]}")
    print(f"\tStocks Ask: {v[4]}")
    print(f"\tOption's Ask: {v[6]}")
    print(f"\tIn the Money: {v[3]}")
   
    k = growth_by_dollar(float(v[9]),float(v[10]),r)
    k = time_decay(float(v[6]),float(v[11]),r)
    k = vega(float(v[6]),float(v[12]),r)
     
# Delta
def growth_by_dollar(delta,gamma,r):
  a = delta
  b = delta
  n = 1
  print("\n-- Underlying Stock Changes (Gamma): -- ")
  while n <= r :
    a += abs(gamma)
    print(f"\tUp ${n}, Delta = {a : .2f}")
    b += abs(gamma)
    if b < 0:
      b = b * -1
    print(f"\tDown ${n}, Delta = {b : .2f}\n")
    n += 1
  return (a,b)
# Theta
def time_decay(value,theta,r):
  print("\n-- Time Decay By Day (Theta): -- ")
  n = 1
  while n <= r:
    value += (theta)
    print(f"\tDay {n} Days from Today: {value : .2f}")
    n +=1 
  print()
  return value
# Vega
def vega(value,vega,r):
  print(f"\n-- Volatility change by 1 percentage point (Vega): --")
  a = value
  b = value
  n = 1
  while n <= r:
    a += vega
    print(f"\t+{n}%: {a : .2f} premium")
    b -= vega
    print(f"\t-{n}%: {b : .2f} premium\n")
    n += 1
  return 0
    
# Create function to be able to calculate all of them at once!


  
    

  
if __name__ == "__main__":
  x = input("\nWhat type? (CALL or PUT):  ")
  y = input("How Many Days Forcasted? ")
  dict = import_from_csv(x)
  data_handler(dict,int(y))

