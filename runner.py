import csv
from datetime import date
from collections import OrderedDict

today = date.today() 
today = str(today)

quotes = {}
fundamentals = {}

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

  with open(f'./{today}/{today[5:]}\'s fundamentals.csv', mode='r') as fs:
      reader = csv.reader(fs)
      for row in reader:
          description = row[0]
          Exchange = row[1]
          EPS = row[2]
          Beta = row[3]
          PE_Ratio = row[4]
          High52 = row[5]
          Low52 = row[6]
          MarketCap = row[7]
          MarketCapFloat = row[8]
          fundamentals.update({description : (description, Exchange, EPS, Beta, PE_Ratio,High52,Low52,MarketCap,MarketCapFloat)})
        
          
  dict1 = OrderedDict(sorted(quotes.items()))
  dict2 = OrderedDict(sorted(fundamentals.items()))
  with open(f'./{today}/{today[5:]}.txt', 'w+') as fst:
    for (key,value), (k2,v2) in zip(dict1.items(), dict2.items()):
        fst.write(f'{key}\n')
        fst.write(f'Exchange: {v2[1]}\n')
        fst.write(f'Open: {value[1]}\n')
        fst.write(f'Bid: {value[2]}\n')
        fst.write(f'Ask: {value[3]}\n')
        fst.write(f'Net Change: {value[4]}%\n')
        fst.write(f'PE_Ratio: {v2[4]}\n')
        if not len(value[4])> 12: 
          temp = float(value[4]) * 100
          fst.write(f'Earning\'s Per share: {temp}\n')
        if not len(value[5])> 12: 
          temp = float(value[5]) * 100
          fst.write(f'Earning\'s Per share: {temp}%\n')
        fst.write(f'Beta: {v2[3]}\n')
        fst.write(f'High52: {v2[5]}\n')
        fst.write(f'Low52: {v2[6]}\n')
        fst.write(f'MarketCap: {v2[7]}\n')
        fst.write(f'MarketCap Float: {v2[8]}\n')
        fst.write(k2 + '\n\n\n')

    



# Runner
if __name__ == "__main__":
  import_from_csv()
  print("DONE!\n")