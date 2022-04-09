import csv
from datetime import date
from collections import OrderedDict
import os
import time
# Variable
path = "Quick"
exist = os.path.exists(path)
if not exist:
  os.makedirs(path)
# Variable
today = date.today() 
today = str(today)
# Variable
quotes = {}
fundamentals = {}
quantitative_analysis = []


# Import CSV data
def import_from_csv():
  with open(f'./{today}/{today[5:]}\'s_quotes.csv', mode='r') as f:
      reader = csv.reader(f)
      for row in reader:
        description = row[0]
        Open = row[1]
        Bid = row [2]
        Ask = row[3]
        Net = row[4]
        NetMarket = row[5]
        quotes.update({description : (description, Open, Bid,Ask,Net,NetMarket)})
  k = 0
  with open(f'./{today}/{today[5:]}\'s fundamentals.csv', mode='r') as fs:
      reader = csv.reader(fs)
      for row in reader:
          k += 1
          description = row[0]
          Exchange = row[1]
          EPS = row[2]
          Beta = row[3]
         
          PE_Ratio = row[4]
          if k >= 2:
            PE_Ratio = float(row[4])
            quantitative_analysis.append((description,PE_Ratio))
          High52 = row[5]
          Low52 = row[6]
          MarketCap = row[7]
          MarketCapFloat = row[8]
          DividendPayAmount = row[9]
          DividendPayDate = row[10]
          NetProfitMarginTTM = row[11]
          fundamentals.update({description : (description, Exchange, EPS, Beta, PE_Ratio,High52,Low52,MarketCap,MarketCapFloat,DividendPayAmount,DividendPayDate,NetProfitMarginTTM)})
        
          
  dict1 = OrderedDict(sorted(quotes.items()))
  with open(f'./Quick/{today[5:]} quotes.txt', 'w+') as fst:
    for (key,value) in dict1.items():
        fst.write(f'{key}\n')
        fst.write(f'Exchange: {value[0]}\n')
        fst.write(f'Open: {value[1]}\n')
        fst.write(f'Bid: {value[2]}\n')
        fst.write(f'Ask: {value[3]}\n')
        if len(value[4]) < 10: 
          net_change = float(value[4])
          fst.write(f'Net Change: {net_change :0.2f}%\n')
        fst.write(key + '\n\n\n')
  time.sleep(1)
  dict2 = OrderedDict(sorted(fundamentals.items()))
  with open(f'./Quick/{today[5:]} fundamentals.txt', 'w+') as fst1:
    for (k,v2) in dict2.items():
        fst1.write(f'Exchange: {v2[0]}\n')
        fst1.write(f'PE_Ratio: {v2[4]}\n')
        if not len(value[5])> 12: 
          temp = float(value[5]) * 100
          fst1.write(f'Earning\'s Per share: {temp}%\n')
        fst1.write(f'Beta: {v2[3]}\n')
        fst1.write(f'High52: {v2[5]}\n')
        fst1.write(f'Low52: {v2[6]}\n')
        fst1.write(f'MarketCap: {v2[7]}\n')
        fst1.write(f'MarketCap Float: {v2[8]}\n')
        fst1.write(f'Dividend Pay Ammount: {v2[9]}\n')
        fst1.write(f'Dividend Pay Date: {v2[10][:11]}\n')
        fst1.write(f'Net Profit Margin TTM: {v2[11]}\n')
        fst1.write(k + '\n\n\n')





# Sort based on PE Ratio
def quantative_value():
  quantitative_analysis.sort(key = lambda x: x[1]) 
  for x in quantitative_analysis:
    print(f'{x[1]} : {x[0]}')

# Runner
if __name__ == "__main__":
  import_from_csv()
  time.sleep(0.5)
  quantative_value()
  print("DONE!\n")