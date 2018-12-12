# -*- coding: utf-8 -*-
"""ccxtrest
  core module.
 
  - Author:     Daniel J. Umpierrez
  - License:    UNLICENSE
  - Created:    13-11-2018
  - Modified:   13-11-2018
"""
from collections import UserDict

import ccxt
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


class Exchanges(UserDict):

    def __init__(self, *exchanges):
        settings = {'timeout': 15000}

        super().__init__(**{e: getattr(ccxt, e)(settings) for e in exchanges if e in ccxt.exchanges})

    def __getattr__(self, item):
        return self.data[item]


selected = dict(binance='binance', crytopia='cryptopia', hitbtc2='hitbtc2')

API = Exchanges(*selected)


@app.route('/ticker/<exchange>/', methods=['GET'])
def get_ticker(exchange):
    symbol = str(request.args.get('symbol')).replace('_', '/')
    data = API[exchange].fetch_tickers(symbol)
    return jsonify(data)


@app.route('/ohlc/<exchange>/', methods=['GET'])
def get_ohlcv(exchange):
    args = dict(limit=25, timeframe='15m')
    args.update(symbol=request.args.get('symbol'), **args)
    data = API[exchange].fetch_ohlcv(**args)
    return jsonify(data.to_dict().values())


@app.route('/book/<exchange>/', methods=['GET'])
def get_orderbook(exchange):
    limit = request.args.get('limit', 5)
    symbol = str(request.args.get('symbol')).replace('_', '/')

    data = API[exchange].fetch_order_book(symbol=symbol, limit=limit)
    if data is None or not isinstance(data, (list, dict)):
        raise TypeError('Invalid {} type.'.format(str(data)))
    elif isinstance(data, dict):
        data = [data]
    else:
        data = [{k: v for k, v in d.items() if k not in 'info'} for d in data]
    return jsonify(data)


@app.route('/market/<exchange>/', methods=['GET'])
def get_markets(exchange):
    symbol = str(request.args.get('symbol')).replace('_', '/')
    markets = API[exchange].markets
    return jsonify(markets.get(symbol))

    # now exchanges dictionary contains all exchange instances...


if __name__ == '__main__':
    app.run()
