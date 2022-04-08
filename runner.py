import csv
from datetime import date

today = date.today()
today = str(today)
map = {}
with open(f'{today[5:]}\'s_quotes.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
      description = row[0]
      Open = row[1]
      Bid = row [2]
      Ask = row[4]
      Net = row[5]
      map.update({description : (description, Open, Bid,Ask,Net)})


for x in map:
  print(x)