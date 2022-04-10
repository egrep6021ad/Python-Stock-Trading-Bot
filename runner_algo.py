import math
def runner_algo(candle_stick,today,minimum_days_momentum,input_dollars):
  with open(f'./Quick/{today[5:]} candle_read.txt', 'w+') as fst2:
    breakout = 0 
    last_high = 0
    breakout = candle_stick.get('1')
    breakout = float(breakout[2])
    count = 0
    bool = 0
    k = ""
    dollars_arr = {}
    for (key,value) in candle_stick.items():
      t = value[3]
      if t != k:
        k = value[3]
        dollars = input_dollars
      try:
        if  float(value[1]) >= breakout: 
          if  float(value[1]) > last_high:
            count += 1
      
            if count >= minimum_days_momentum:
              breakout = float(value[1])
              if count == minimum_days_momentum:
              
                if bool == 0 and float(value[1])<= dollars:
                  bool = 1
                  fst2.write(f"\nBUY {value[3]}! --> ({count} Day Increase):\n")
                  fst2.write(f'Current Days High: ${value[1]}\n')
                  multiplier = math.floor(dollars / float(value[1]))
                  if multiplier > 1:
                    dollars = dollars - (float(value[1]) * multiplier)
                  else:
                    multiplier = 1
                    if float(value[1]) < dollars:
                      dollars = dollars - (float(value[1]) * multiplier)
                  print(f"\nAfter Buy: {dollars:0.2f} ({value[3]})")
                  print(f"\tPrice per share: {value[1]}")
                  print(f"\tShares: {multiplier}")
                fst2.write(f"{value[4]}\n")
                change_perc = get_inc_percentage(value[1],last_high)
                fst2.write(f'Percentage Change +{change_perc:0.2f}%\n')
              
              else:
                fst2.write(f"\nHOLD Day: {str(count-minimum_days_momentum)} ({str(count)} Days Since Buy Indicator)\n")
                change_perc = get_dec_percentage(value[1],last_high)
                change_perc = change_perc * -1
                fst2.write(f"Percent Change: {change_perc :0.2f}%\n")
              fst2.write(f'Previous Days High: {last_high}\n\n')
                            
            last_high = float(value[1])
          else:
            count = 0
            last_high = breakout
        
        elif float(value[1]) < breakout:
          change_perc =  get_dec_percentage(value[1],last_high)
          breakout = float(value[1])
          count = 0
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
      dollars_arr.update({value[3]:dollars})
  temp = 0
  temp2 = 0
  print(f"\nStart: $ {input_dollars} Each TICKR")
  for (key,value) in dollars_arr.items():
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

def get_inc_percentage(a,b):
  a = float(a)
  b = float(b)
  return ((a-b)/abs(b) ) * 100

def get_dec_percentage(a,b):
  a = float(a)
  b = float(b)
  return ((b-a)/abs(b) ) * 100