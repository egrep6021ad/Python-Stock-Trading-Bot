import math
from pprint import pprint
def runner_algo(candle_stick,           # Dictionary with TCKR history
                today,                  # Date
                min_momentum,           # Min days trending to purchase 
                input_dollars ):        # Money per asset

  # Global Variable Init. 
  support = float(candle_stick.get('0')[2]) 
  end_of_file = list(candle_stick.items())[-2][1][0]
  days_trending = 0           
  invested = False                     
  prev_symbol = ""                     
  portfolio = {}  
  daily_high_arr = [1]
  date_arr = []
  shares = 1
  funds_remain = input_dollars

                  
  with open(f'./Quick/{today[5:]} candle_read.txt', 'w+') as fst2:
    # Iterate though every entry ("Candle Stick")
    for (key,value) in list(candle_stick.items())[1:-1]:
      
      # Get TICKR Symbol & CURRNT day HIGH
      symbol = value[3]
      date_arr.append(value[4])
      daily_high_arr.append(float(value[1]))
      curr_high = daily_high_arr[-1]
  
      if symbol != prev_symbol: # SYMBOL (asset) CHANGE:
        if invested == True:
          # SELL! TIME line is ended (next stock is starting)..
          sell_function = sell_asset(invested,fst2,funds_remain,daily_high_arr[-2], shares,date_arr[-1],prev_symbol)
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
                  asset = buy_asset(today,value,curr_high,days_trending,funds_remain,invested)
                  invested = True
                  funds_remain = asset[0]
                  shares = asset[1]
                  fst2.write(f"\nBUY {value[3]}\n")
                  fst2.write(f"{value[4]}\n")
                  fst2.write(f"{curr_high}\n\n")
                  portfolio.update({symbol : funds_remain})
            # HOLD
            elif funds_remain != input_dollars:
              fst2.write(f"\nHOLD {value[4]}\n")
          days_trending += 1            
        
      # Fell throuh support
      else:
        support = curr_high
        days_trending = 0
        mean = [1]
        change = percent_change(daily_high_arr[-2],curr_high,mean)
        change = change[0]
        if change > 0.5:
          # SELL! assets have fallen ___% far...
          sell_function = sell_asset(invested,fst2,funds_remain,curr_high, shares,value[4],prev_symbol)
          invested = sell_function[0]
          funds_remain = sell_function[1] 
          portfolio.update({symbol : funds_remain})


  # END: Cumulative data ->  txt file
  with open(f'./Quick/{today[5:]} candle_read.txt', 'a') as fst2:     
  # Print The statistics
    cash_out=0
    cash_in = 0
    fst2.write(f"\nStart: $ {input_dollars} Each symbol\n")
    for (symbol,dollar_value) in portfolio.items():
      #fst2.write(f'day_day_perc_change{symbol}: $ {dollar_value:0.2f}\n')
      cash_out += dollar_value
      cash_in += 1
    fst2.write(f"\nInvested: {str(input_dollars*cash_in)}\n")  
    fst2.write(f"Returned: {cash_out:0.2f}\n")
    fst2.write(f"Profit: $ {cash_out-input_dollars*cash_in:0.2f}\n")
    change = percent_change(cash_in*input_dollars,cash_out,[1])
    change = change[0]
    fst2.write(f"Change: {change : 0.2f} (negative = % growth, positive = % loss)\n")
    print("\n")
    pprint(portfolio)
  return



# Helper function
def percent_change(a,b,mean):
  c =((a-b)/abs(b)) * 100
  return (c,mean)

# BUY Function
def buy_asset(today,value,curr_high,days_trending,funds_remain,invested):
  with open(f'./Quick/{today[5:]} candle_read.txt', 'a') as fst2:
    fst2.write(f"\nBUY {value[3]}! --> ({days_trending} Day Increase):\n")
    fst2.write(f'Current Days High: ${curr_high}\n')
    # Calculate how many shares can be purchased
    multiplier = math.floor(funds_remain / float(curr_high))
    # If at lease 1 share can be bought...
    if multiplier > 1:
      funds_remain = funds_remain - curr_high * multiplier
    else:
      funds_remain = funds_remain - curr_high
  return (funds_remain,multiplier)


# SELL Function
def sell_asset(invested,fst2,funds_remain,curr_high, shares,date,prev_symbol):
  # SELL! assets have fallen ___% far...
  if invested == True: 
    invested = False
    fst2.write(f"\n*** SELL: {prev_symbol} @ ${curr_high}\n")
    funds_remain = funds_remain + curr_high * shares
    fst2.write(f"{date}\n")
  return (invested, funds_remain)