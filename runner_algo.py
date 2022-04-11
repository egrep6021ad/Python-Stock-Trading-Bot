import math

def runner_algo(candle_stick,           # Dictionary with TCKR history
                today,                  # Date
                min_momentum,           # Min days trending to purchase 
                input_dollars ):        # Money per asset
                 
  with open(f'./Quick/{today[5:]} candle_read.txt', 'w+') as fst2:
    prev_day_high = 0
    support = float(candle_stick.get('0')[2])  # The first element's LOW = ENTRY point
    days_trending = 0                        # Track days to see when min. is satisfied
    invested = False                      # Determines which direction data is trending
    prev_symbol = ""                        # Track when SYMBOL changes
    portfolio = {}                     # Track returns per asset
    daily_high_arr = [0]
    shares = 1
    mean = []
    
    # Starting funds:
    funds_remain = input_dollars
    end = list(candle_stick.items())[-2][1][0]
  
   
    # Iterate though every entry ("Candle Stick")
    for (key,value) in list(candle_stick.items())[1:-1]:
      
      # Get Symbol & current day HIGH
      symbol = value[3]  
      daily_high_arr.append(float(value[1]))
      curr_high = daily_high_arr[-1]
      
      # SYMBOL (asset) CHANGE:
      if symbol != prev_symbol:
        prev_symbol = value[3]
        funds_remain = input_dollars
        invested = False
        support = 0
        prev_day_high = curr_high
    
      # START:
     
      k = percent_change(prev_day_high,curr_high,mean)
      day_day_perc_change = k[0]
      mean = k[1]
      deviation = 0
      try:
        deviation = (sum(mean)/len(mean)  - abs(day_day_perc_change)) / day_day_perc_change* 100
        print(f'Z : {deviation}\n')
      except ZeroDivisionError:
        print("ZeroDivisionError")
        
      if curr_high >= support and value[0] != end:   
        if deviation > -170: 
          days_trending += 1         
          if days_trending >= min_momentum:  
            support =  daily_high_arr[-2] # Support becomes the High 2 days prior to current
            
            # BUY soon as min. momentum is met & there is enough money
            if days_trending == min_momentum:  
                if invested == False and curr_high<= funds_remain:
                  asset = buy_asset(today,value,curr_high,days_trending,funds_remain,invested)
                  invested = True
                  funds_remain = asset[0]
                  shares = asset[1]
                  fst2.write(f"\nBUY {value[3]}\n")
                  fst2.write(f"{value[4]}\n")
                  fst2.write(f"{curr_high}\n\n")
            # HOLD
            else:
              fst2.write(f"\nHOLD {value[4]}\n")
              fst2.write(f'Previous Days High: {prev_day_high}\n\n')
                      
          prev_day_high = curr_high
        # Otherwise, were not trending up, but above resistance  
        else:
          days_trending = 0
          prev_day_high = support
          support = curr_high
          # SELL! assets have fallen ___% far...
          if invested == True: # This stops from small changes
            invested = False
            fst2.write(f"\day_day_perc_change*** SELL: {value[3]} @ ${curr_high}\n")
            funds_remain = funds_remain + curr_high * shares
            fst2.write(f"\day_day_perc_change\day_day_perc_change{value[4]}\n")

           
      # Fell throuh support
      else:
          support = 0
          days_trending = 0
          # SELL! assets have fallen ___% far...
          if invested == True: # This stops from small changes
            invested = False
            fst2.write(f"\tSELL: {value[3]} @ ${curr_high}\n")
            funds_remain = funds_remain + curr_high * shares
            fst2.write(f"\day_day_perc_change\day_day_perc_change{value[4]}\n")
      
            
      # update { $SYM : New Balance afer transaction}
      portfolio.update({value[3]:funds_remain})

  # END: Cumulative data ->  txt file
  
 
  with open(f'./Quick/{today[5:]} candle_read.txt', 'a') as fst2:     
  # Print The statistics
    cash_out=0
    cash_in = 0
    fst2.write(f"\nStart: $ {input_dollars} Each symbol\n")
    for (symbol,dollar_value) in portfolio.items():
      fst2.write(f'\day_day_perc_change{symbol}: $ {dollar_value:0.2f}\n')
      cash_out += float(dollar_value)
      print(float(dollar_value))
      cash_in += 1
    fst2.write(f"\nInvested: {str(input_dollars*cash_in)}\n")  
    fst2.write(f"Returned: {cash_out:0.2f}\n")
    fst2.write(f"Profit: $ {cash_out-input_dollars*cash_in:0.2f}\n")
   
    print(portfolio)
 

  return

# Helper function

# Helper function


def percent_change(a,b,mean):
  a = float(a)
  b = float(b)
  c =((a-b)/abs(b)) * 100
  if c != -100:
    mean.append(c)
    print(sum(mean)/len(mean))
  print(f'a: {a}')
  print(f'b: {b}')
  print(c)
  

  
  return (c,mean)

#Helper Function
def buy_asset(today,value,curr_high,days_trending,funds_remain,invested):
  with open(f'./Quick/{today[5:]} candle_read.txt', 'a') as fst2:
    #invested = True
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