import math
def runner_algo(candle_stick, # Dictionary with TCKR history
                today,        # Date
                minimum_days_momentum, # Min days trending to purchase 
                input_dollars          # Money per asset
               ):
  with open(f'./Quick/{today[5:]} candle_read.txt', 'w+') as fst2:
    breakout = 0 
    last_high = 0
    breakout = candle_stick.get('1')# The first element will set..
    breakout = float(breakout[2]) # resistance / base - line
    count = 0                     # Track days to see when min. is satisfied
    bool = 0                      # Determines which direction data is trending
    k = ""                        # Track when SYMBOL changes
    dollars_dict = {}             # Track returns per asset

    # Iterate though every entry ("Candle Stick")
    for (key,value) in candle_stick.items():
      t = value[3]  # Track when the SYMBOL (asset) changes
      if t != k:
        k = value[3]
        dollars = input_dollars  # If it changes, allot it's full ammount
      try:
        if  float(value[1]) >= breakout:     # Daily high > resistance
          if  float(value[1]) > last_high:   # Daily high > previous high
            count += 1                       # Trending...
            if count >= minimum_days_momentum:  # If min. days trending = satisfied
              breakout = float(value[1])        # Set new resistance / base-line

              # As soon as min. momentum is met & there is enough money -> BUY
              if count == minimum_days_momentum:  
                if bool == 0 and float(value[1])<= dollars:
                  # Change direction  
                  bool = 1
                  fst2.write(f"\nBUY {value[3]}! --> ({count} Day Increase):\n")
                  fst2.write(f'Current Days High: ${value[1]}\n')
                  # Calculate how many shares can be purchased
                  multiplier = math.floor(dollars / float(value[1]))
                  # If at lease 1 share can be bought...
                  if multiplier > 1:
                    dollars = dollars - (float(value[1]) * multiplier)
                  
                  else:
                    # Since rounding down it could be 0, so set as 1 & check again...
                    multiplier = 1
                    # If one share can be bought, buy it
                    if float(value[1]) < dollars:
                      dollars = dollars - (float(value[1]) * multiplier)
                  print(f"\nAfter Buy: {dollars:0.2f} ({value[3]})")
                  print(f"\tPrice per share: {value[1]}")
                  print(f"\tShares: {multiplier}")
                fst2.write(f"{value[4]}\n")
                change_perc = get_inc_percentage(value[1],last_high)
                fst2.write(f'Percentage Change +{change_perc:0.2f}%\n')
              # Holding (post purchase)
              else:
                fst2.write(f"\nHOLD Day: {str(count-minimum_days_momentum)} ({str(count)} Days Since Buy Indicator)\n")
                change_perc = get_dec_percentage(value[1],last_high)
                change_perc = change_perc * -1
                fst2.write(f"Percent Change: {change_perc :0.2f}%\n")
              fst2.write(f'Previous Days High: {last_high}\n\n')
            # Last high is always previous day!             
            last_high = float(value[1])
          # Otherwise, were not trending up, but above resistance  
          else:
            count = 0
            last_high = breakout
        # Broke throuh resistance
        elif float(value[1]) < breakout:
          change_perc =  get_dec_percentage(value[1],last_high)
          breakout = float(value[1])
          count = 0
          # If we have assets, and weve fallen ___% far...SELL
          if bool == 1 and change_perc>0.5: # working KEY ONE! This stops from small changes
            bool = 0
            fst2.write(f"\tSELL: {value[3]} @ ${value[1]}\n")
            dollars = dollars + (float(value[1]) * multiplier)
            print(f"After Sell: {dollars:0.2f} ({value[3]})")
            print(f"\tPrice per share: {value[1]}")
            print(f"\tShares: {multiplier}\n")
          fst2.write(f"\t\t{value[4]}\n")
          change_perc =  get_dec_percentage(value[1],last_high)
          fst2.write(f'\t\t<----- Decreasing\n')
          fst2.write(f'\t\tChange from support line (swing low): -{change_perc:0.2f}%\n\n')
         
      except ValueError:
         print("Value error")
         continue
      except TypeError:
         print("Type error")
         continue
      dollars_dict.update({value[3]:dollars})
      
  # Print The statistics
  temp = 0
  temp2 = 0
  print(f"\nStart: $ {input_dollars} Each TICKR")
  for (key,value) in dollars_dict.items():
    print(f'\t{key}: $ {value:0.2f}')
    temp += float(value)
    temp2 += 1
  print(f"\nInvested: {str(input_dollars*temp2)}")  
  print(f"Returned: {temp:0.2f}")
  print(f"Profit: $ {temp-input_dollars*temp2:0.2f}")
  change_perc = get_dec_percentage(temp,(input_dollars * temp2))
  change_perc = change_perc * -1
  print(f"Change: {change_perc:0.2f} %\n")
  return

# Helper function
def get_inc_percentage(a,b):
  a = float(a)
  b = float(b)
  return ((a-b)/abs(b) ) * 100
# Helper function
def get_dec_percentage(a,b):
  a = float(a)
  b = float(b)
  return ((b-a)/abs(b) ) * 100