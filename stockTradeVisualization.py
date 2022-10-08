import os
import matplotlib.pyplot as plt
import csv
from datetime import date

today = date.today()
today = str(today)

sell_date, buy_date, sell_price, buy_price = [], [], [], []
count = 0

with open(f'./recentTrades/{today[5:]} stock_buy.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        buy_price.append(float(row[2]))
        buy_date.append(row[3])
        count += 1

with open(f'./recentTrades/{today[5:]} stock_sell.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        sell_price.append(float(row[2]))
        sell_date.append(row[3])
        count += 1

with open(f'./recentTrades/{today[5:]} candle_read.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        invested = row[0]
        returned = row[1]
        profit = row[2]


fig, ax = plt.subplots()
ax.plot(buy_date, buy_price, label='Prices 2008-2018', color='blue')
ax.plot(sell_date, sell_price, label='Prices 2010-2018', color = 'red')
legend = ax.legend(loc='center right', fontsize='x-large')
plt.xlabel('years')
plt.ylabel('prices')
plt.title('Comparison of the different prices')
plt.savefig('tradeReport.png')

'''

plt.figure(figsize=(15, 15))
plt.plot(buy_date,
         buy_price,
         color='g',
         linestyle='none',
         marker='o',
         label='Buy')

plt.plot(sell_date,
         sell_price,
         color='r',
         linestyle='none',
         marker='o',
         label="Sell")

plt.xticks(rotation=90)
plt.xlabel('Dates')
plt.ylabel('Price($)')
plt.title('Trade Report', fontsize=20)
plt.grid()
plt.legend()

plt.savefig('tradeReport.png')
'''
