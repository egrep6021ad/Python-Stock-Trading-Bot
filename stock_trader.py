import math
from pprint import pprint
import csv
from datetime import date
import os
today = date.today()
today = str(today)

path = f"./Quick"
exist = os.path.exists(path)
if not exist:
  os.makedirs(path)
  
def runner_algo( min_momentum,           # Min days trending to purchase 
                input_dollars ):        # Money per asset
  candle_stick = get_data()
  # Global Variable Init. 
  #support = float(candle_stick.get('0')[2]) 
  end_of_file = list(candle_stick.items())[-1][1][0]
  days_trending = 0           
  invested = False                     
  prev_symbol = ""                     
  portfolio = {}  
  daily_high_arr = [1]
  date_arr = []
  shares = 1
  funds_remain = input_dollars

                  
  with open(f'./Quick/{today[5:]} stock_buy.csv', 'w+') as fst2:
    # Iterate though every entry ("Candle Stick")
    writer = csv.writer(fst2)
    for (key,value) in list(candle_stick.items()):
      
      # Get TICKR Symbol & CURRNT day HIGH
      symbol = value[3]
      date_arr.append(value[4])
      daily_high_arr.append(float(value[1]))
      curr_high = daily_high_arr[-1]
  
      if symbol != prev_symbol: # SYMBOL (asset) CHANGE:
        if invested == True:
          # SELL! TIME line is ended (next stock is starting)..
          sell_function = sell_asset(invested,writer,funds_remain,daily_high_arr[-2], shares,date_arr[-1],prev_symbol)
          invested = sell_function[0]
          funds_remain = sell_function[1]
          portfolio.update({ prev_symbol : funds_remain})
        prev_symbol = value[3]
        funds_remain = input_dollars
        invested = False
        support = 0
        
      # START:
      if curr_high >= support and value[0] != end_of_file: 
          if days_trending >= min_momentum:  
            support = daily_high_arr[-2] # Support becomes the High 2 days prior to current
            # BUY soon as min. momentum is met & there is enough money
            if days_trending == min_momentum:  
                if invested == False:
                  asset = buy_asset(curr_high,funds_remain)
                  invested = True
                  funds_remain = asset[0]
                  shares = asset[1]
                  temp = ("BUY", value[3],curr_high,value[4])
                  writer.writerow(temp)
                  portfolio.update({symbol : funds_remain})
            # HOLD
           # elif funds_remain != input_dollars:
          days_trending += 1            
        
      # Fell throuh support
      else:
        support = curr_high
        days_trending = 0
        mean = [1]
        change = percent_change(daily_high_arr[-2],curr_high,mean)
        change = change[0]
        if change > 0.25 or value[0] == end_of_file:
          # SELL! assets have fallen ___% far...
          sell_function = sell_asset(invested,writer,funds_remain,curr_high, shares,value[4],prev_symbol)
          invested = sell_function[0]
          funds_remain = sell_function[1] 
          portfolio.update({symbol : funds_remain})


  # END: Cumulative data ->  txt file
  with open(f'./Quick/{today[5:]} candle_read.csv', 'w+') as fst2:     
  # Print The statistics
    writer = csv.writer(fst2)
    cash_out=0
    cash_in = 0
    for (symbol,dollar_value) in portfolio.items():
      #fst2.write(f'day_day_perc_change{symbol}: $ {dollar_value:0.2f}\n')
      cash_out += dollar_value
      cash_in += 1

    invested = str(input_dollars*cash_in)
    returned = f'{cash_out:0.2f}'
    profit = f"{cash_out-input_dollars*cash_in:0.2f}"
    change = percent_change(cash_in*input_dollars,cash_out,[1])
    change = f"{change[0] : 0.2f}"
    temp = (invested,returned,profit,change)
    writer.writerow(temp)
    print("\n")
    pprint(portfolio)
  return



# Helper function
def percent_change(a,b,mean):
  c =((a-b)/abs(b)) * 100
  return (c,mean)

# BUY Function
def buy_asset(curr_high,funds_remain):
  # Calculate how many shares can be purchased
  multiplier = math.floor(funds_remain / float(curr_high))
  # If at lease 1 share can be bought...
  if multiplier > 1:
    funds_remain = funds_remain - curr_high * multiplier
  else:
    funds_remain = funds_remain - curr_high
  return (funds_remain,multiplier)


# SELL Function
def sell_asset(invested,writer,funds_remain,curr_high, shares,date,prev_symbol):
  with open(f'./Quick/{today[5:]} stock_sell.csv', 'a+') as fst2:
    # Iterate though every entry ("Candle Stick")
    writer = csv.writer(fst2)
    if invested == True: 
      invested = False
      funds_remain = funds_remain + curr_high * shares
      temp = ("SELL", prev_symbol, curr_high, date)
      writer.writerow(temp)
  return (invested, funds_remain)


# Data Source
def get_data():
  candle_stick = {}
  k = 0
  with open(f'./{today}/{today[5:]}\'s candle_stick.csv', mode='r') as fs:
    reader = csv.reader(fs)
    for row in reader:
        if k >= 1:
          days = row[0]
          high = row[3]
          low = row[4]
          sym = row[6]
          date = row[7]
          candle_stick.update({days: (days,
                                      high,
                                      low,
                                      sym,
                                      date)
                              })
        k += 1
  return candle_stick

if __name__ == "__main__":
  runner_algo(1,10000)