import requests
from datetime import datetime
import csv, os
from datetime import date

#today = str(date.today())
os.environ['TZ'] = ('US/EASTERN')


def getHistory(ticker, td_consumer_key, period_type, period, freq_type):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

    candleStick_dict = {}

    num = 0
    for i in ticker:
        full_url = endpoint.format(stock_ticker=i,
                                   periodType=period_type,
                                   period=period,
                                   frequencyType=freq_type,
                                   frequency=1)
        page = requests.get(url=full_url, params={'apikey': td_consumer_key})
        #content = json.loads(page.content)
        data = page.json()
        temp = data['candles']
        sym = f"${data['symbol']}"
        for x in temp:
            curr_date = float(x['datetime'])
            curr = datetime.utcfromtimestamp(curr_date /
                                             1000).strftime('%D-%M-%Y-')
            curr = (curr[0:9] + curr[12:-1])
            z = (num, x['open'], x['close'], x['high'], x['low'], x['volume'],
                 sym, curr)
            candleStick_dict.update({num: z})
            num += 1
    # Write stock price history to CSV:
    if not os.path.isdir(f'./{str(date.today())}'):
        os.mkdir(f'./{str(date.today())}')
    with open(
            f'./{str(date.today())}/{str(date.today())[5:]}\'s candle_stick.csv',
            'w+') as f:
        writer = csv.writer(f)
        for x in candleStick_dict:
            writer.writerow(candleStick_dict[x])
