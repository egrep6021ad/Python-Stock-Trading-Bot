#from flask import Flask
import os
import matplotlib.pyplot as plt
import csv
from datetime import date

today = date.today()
today = str(today)

#os.system("python data_miner.py")
#os.system("python stock_trader.py")
#os.system("python options_trader.py")

x = []
y = []
t = []
z = []
count = 0
k = []
with open(f'./Quick/{today[5:]} stock_buy.csv','r') as csvfile:
  lines = csv.reader(csvfile, delimiter=',')
  for row in lines:
    x.append(row[3])
    y.append(float(row[2]))
    count += 1

with open(f'./Quick/{today[5:]} stock_sell.csv','r') as csvfile:
  lines = csv.reader(csvfile, delimiter=',')
  for row in lines:
    t.append(row[3])
    z.append(float(row[2]))
    count += 1

with open(f'./Quick/{today[5:]} candle_read.csv','r') as csvfile:
  lines = csv.reader(csvfile, delimiter=',')
  for row in lines:
    invested = row[0]
    returned = row[1]
    profit = row[2]
    


plt.figure(figsize=(15,15))
plt.plot(x,y, color = 'g', linestyle = 'none',
		marker = 'o',label='Buy')

plt.plot(z, color = 'r', linestyle = 'none',
	marker = 'o',label = "Sell")


plt.xticks(rotation = 90)
plt.xlabel('Dates')
plt.ylabel('Price($)')
plt.title('Trade Report', fontsize = 20)
plt.grid()
plt.legend()

plt.savefig('tradeReport.png')

