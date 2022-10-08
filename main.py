#from flask import Flask
import os
from datetime import date
import fetch_biggestDailyMovers
import fetch_stockPriceHistory
import stockTradingBot

def gatherData():
    # Specify path for new files:
    path = f"./{str(date.today())}"
    # Check if files exist:
    exist = os.path.exists(path)
    if not exist:
        os.makedirs(path)
    # API key: 
    my_secret = os.environ['hulcrux']
    _key = my_secret
    try:
      # Returns array of SYMBOLS for days biggest movers:
      user_input = input("Do you want to get the days top 5 movers? (Y/N) ")
      if user_input == 'Y':
        arr = fetch_biggestDailyMovers.getMovers(_key)
        arr = arr[0:5]
      else:
        user_input = input("Enter the TICKR of the desired stock (i.e. TSLA): ")
        arr = [user_input]
      # Verify TICKR symbols for user:
      print(f"Assessing: {arr}")
    except KeyError:
      print("Key Error!")
    print("DONE")
    return [arr, _key]

  
def runStockTradingBot(arr, _key):
    total_investment = 0
    current_portfolio_value = 0
    for x in arr:
      total_investment += 10000
      fetch_stockPriceHistory.getHistory([x], _key)
      current_portfolio_value += stockTradingBot.runner_algo(1, 10000)
    print(total_investment)
    print(current_portfolio_value)
    return (total_investment, current_portfolio_value)

if __name__ == "__main__":
  data = gatherData()
  results = runStockTradingBot(data[0], data[1])


  
'''
app = Flask('app')
@app.route('/')
def index():
  return f'<h1>{data[0]}<hr>{results[0]}<br>{results[1]}</h1>'
  
app.run(host='0.0.0.0', port=8080)
'''

  