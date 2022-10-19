from flask import Flask, jsonify, request
import os
from datetime import date
import fetch_biggestDailyMovers
import fetch_stockPriceHistory
import stockTradingBot
from flask_cors import CORS

app = Flask('app')
CORS(app)
os.environ['TZ'] = ('US/EASTERN')
my_secret = os.environ['hulcrux']
_key = my_secret


def runStockTradingBot(arr, initial_investment, period_type, period,
                       freq_type):
    total_investment = 0
    current_portfolio_value = 0
    for x in arr:
        total_investment += initial_investment
        fetch_stockPriceHistory.getHistory([x], _key, period_type, period,
                                           freq_type)
        current_portfolio_value += stockTradingBot.runner_algo(
            1, initial_investment)
    print(total_investment)
    print(current_portfolio_value)
    return ([total_investment, current_portfolio_value])


@app.route('/userChoice', methods=('GET', 'POST'), strict_slashes=False)
def post_SpecificStockAndTrade():
    if request.method == 'POST':
        # Make the trades based on user symbols:
        try:
            data = request.get_json()
            period_type = ""
            period = ""
            freq_type = "daily"
            if data['TIME'] == '1day':
                period_type = "day"
                period = 1
                freq_type = 'minute'
            if data['TIME'] == '3mos':
                period_type = 'month'
                period = 3
            if data['TIME'] == '6mos':
                period_type = 'month'
                period = 6
            if data['TIME'] == '1yr':
                period_type = 'year'
                period = 1
            # Output = array[invested, finalResult]
            output = runStockTradingBot([data['TICKR']],
                                        int(data['INITIAL INVESTMENT']),
                                        period_type, period, freq_type)
            return jsonify(output)
        except:
            return jsonify("ERROR")


@app.route('/dailyMovers', methods=('GET', 'POST'), strict_slashes=False)
def get_DailyMovers():
    try:
        direction = request.get_json()
        arr = fetch_biggestDailyMovers.getMovers(_key, direction['direction'])
        # Only send top 10:
        arr = arr[0:10]
        return jsonify(arr)
    except:
        d = ["ERR"]
        d = d * 10
        return jsonify(d)


@app.route('/')
def index():
    return "piss off mate"


app.run(host='0.0.0.0', port=7000)
