from flask import Flask, jsonify, request
import os
from datetime import date
import fetch_biggestDailyMovers
import fetch_stockPriceHistory
import stockTradingBot
from flask_cors import CORS

today = date.today()
today = str(today)
os.environ['TZ'] = ('US/EASTERN')
print(today)

def runStockTradingBot(arr):
    # API key:
    my_secret = os.environ['hulcrux']
    _key = my_secret
    total_investment = 0
    current_portfolio_value = 0
    for x in arr:
        total_investment += 10000
        fetch_stockPriceHistory.getHistory([x], _key)
        current_portfolio_value += stockTradingBot.runner_algo(1, 10000)
    print(total_investment)
    print(current_portfolio_value)
    return (total_investment, current_portfolio_value)


app = Flask('app')
CORS(app)
os.environ['TZ'] = ('US/EASTERN')

@app.route('/userChoice', methods=('GET', 'POST'), strict_slashes=False)
def post_SpecificStockAndTrade():
    if request.method == 'POST':
        # Make the trades based on user symbols: 
        try:
          data = request.get_json()
          output = runStockTradingBot([data['TICKR']])
          return jsonify(output)
        except:
          return jsonify("ERROR")
    


@app.route('/dailyMovers')
def get_DailyMovers():
    return "piss off mate"


@app.route('/')
def index():
    return "piss off mate"


app.run(host='0.0.0.0', port=7000)
'''
    try:
        # Returns array of SYMBOLS for days biggest movers:
        user_input = input("Do you want to get the days top 5 movers? (Y/N) ")
        if user_input == 'Y':
            arr = fetch_biggestDailyMovers.getMovers(_key)
            arr = arr[0:5]
        else:
            user_input = input(
                "Enter the TICKR of the desired stock (i.e. TSLA): ")
            arr = [user_input]
        # Verify TICKR symbols for user:
        print(f"Assessing: {arr}")
    except KeyError:
        print("Key Error!")
    print("DONE")
    return [arr, _key]




    def createNewFiles():
    # Specify path for new files:
    path = f"./{str(date.today())}"
    # Check if files exist:
    exist = os.path.exists(path)
    if not exist:
        os.makedirs(path)
'''
