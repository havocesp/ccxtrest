# -*- coding: utf-8 -*-
"""ccxtrest
  core module.
 
  - Author:     Daniel J. Umpierrez
  - License:    UNLICENSE
  - Created:    13-11-2018
  - Modified:   13-11-2018
"""
import typing as tp

import pandaxt
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)
exchange_list = ['hitbtc2', 'cryptopia', 'binance']
exchanges = dict.fromkeys(exchange_list)  # type: tp.Dict[tp.AnyStr, pandaxt.PandaXT]

for ex in exchange_list:
    exchanges[ex] = pandaxt.PandaXT(ex)


# def do_info_drop(data, symbol=None, **kwargs):
#     if symbol and symbol in data:
#         data = data.get(symbol or '', data)
#         if 'info' in data:
#             del data['info']
#     elif isinstance(data, dict):
#         data = {k: {x: y for x, y in v.items() if y and x not in ['info']} for k, v in data.items()}
#     elif isinstance(data, (list, tuple, set)):
#         data = [{x: y for x, y in v.items() if y and x not in ['info']} if isinstance(v, dict) else v for v in data]
#     return data


@app.route('/ticker/<exchange>/', methods=['GET'])
def get_ticker(exchange):
    symbol = str(request.args.get('symbol')).replace('_', '/')
    data = exchanges[exchange].get_tickers(symbol)
    return jsonify(data.data)


@app.route('/ohlc/<exchange>/', methods=['GET'])
def get_ohlcv(exchange):
    args = dict(limit=25, timeframe='15m')
    args.update(symbol=request.args.get('symbol'), **args)
    data = exchanges[exchange].get_ohlc(**args)
    return jsonify(data.to_dict().values())


# noinspection PyUnresolvedReferences
@app.route('/book/<exchange>/', methods=['GET'])
def get_orderbook(exchange):
    args = dict(limit=5)
    args.update(**request.args)
    data = get_exchange(exchange).fetch_order_book(**args)
    return jsonify(do_info_drop(data, **args))


# @app.route('/markets/<exchange>', defaults={'symbol1': None, 'symbol2': None}, methods=['GET'])
@app.route('/market/<exchange>/', methods=['GET'])
def get_markets(exchange):
    symbol = str(request.args.get('symbol')).replace('_', '/')
    markets = exchanges[exchange].markets
    return jsonify(markets.get(symbol))


# now exchanges dictionary contains all exchange instances...
if __name__ == '__main__':
    app.run()
