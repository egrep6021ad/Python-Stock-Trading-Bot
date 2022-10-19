import requests


def getMovers(td_consumer_key, direction):
    movers_url = "https://api.tdameritrade.com/v1/marketdata/{index}/movers"

    movers_symbols = []

    indexes = ['$DJI', '$SPX.X', '$COMPX']
    for i in indexes:
        # Fetch data
        endpoint = movers_url.format(index=i)
        data = requests.get(url=endpoint,
                            params={
                                'apikey': td_consumer_key,
                                'direction': direction
                            })
        # JSON -> Array
        data = data.json()
        for x in data:
            movers_symbols.append([
                x['description'], x['direction'], x['change'],
                x['totalVolume'], x['symbol']
            ])
    return movers_symbols
