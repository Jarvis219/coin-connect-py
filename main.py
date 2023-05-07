from flask import Flask, request, jsonify
from constans import list_coin_API, top_coin_API
from utils import get_date_by_days, get_month_ago, get_year_ago, currentDay, get_date_by_str, coin_by_symbol_API, coinHeaders
from middleware import middleware
import requests
import json

app = Flask(__name__)
app.wsgi_app = middleware(app.wsgi_app)


@app.route('/list-coin')
def list_coin():
    headers = {
        'Content-Type': 'application/json'
    }

    dataGraphql = {
        'query': 'query {\nVN100 {\nstocks(take: 3000) {\nitems {\nsymbol\nbuyPrice3\nbuyVolume3\nbuyPrice2\nbuyVolume2\nbuyPrice1\nbuyVolume1\nchange\ncurrentPrice\ncurrentVolume\ntotalVolume\nsellPrice3\nsellVolume3\nsellPrice2\nsellVolume2\nsellPrice1\nsellVolume1\nhighPrice\nlowPrice\nforeignBuyVolume\nforeignSellVolume\nfloorPrice\nceilPrice\nreferencePrice\nforeignBuyValue\nforeignSellValue\n}\n}\n}\n}',
    }

    try:
        res = requests.post(list_coin_API, headers=headers, json=dataGraphql)
        return jsonify(res.json()['data']['VN100']['stocks']['items'])
    except ValueError:
        return jsonify({"message": "Error"})


@app.route('/top-coins')
def top_coins():
    top_coins = []

    try:
        res_top_coin = requests.get(top_coin_API, headers=coinHeaders)

        for coin in res_top_coin.json():
            res = coin_by_symbol_API(
                coin['symbol'], get_date_by_days(7), currentDay, 1, coinHeaders)
            top_coins.append(res.json()[0])

        return jsonify(top_coins)
    except ValueError:
        return jsonify({"message": "Error"})


@app.route('/coin-by-symbol')
def coin_by_symbol():
    data = json.loads(request.get_data())

    symbol = data['symbol']
    startDate = get_date_by_str(data.get('startDate', get_date_by_days(7)))
    endDate = get_date_by_str(data.get('endDate', currentDay))
    limit = data.get('limit', 1000)
    dayAgo = data.get('dayAgo', None)
    monthAgo = data.get('monthAgo', None)
    yearAgo = data.get('yearAgo', None)

    if (startDate > endDate):
        return jsonify({"message": "Start date must be less than end date"})

    if (dayAgo):
        startDate = get_date_by_days(dayAgo)
        endDate = get_date_by_days(0)

    if (monthAgo):
        startDate = get_month_ago(monthAgo)
        endDate = get_month_ago(0)

    if (yearAgo):
        startDate = get_year_ago(yearAgo)
        endDate = get_year_ago(0)

    startDate = str(startDate).replace('-', '/')
    endDate = str(endDate).replace('-', '/')

    try:
        res = coin_by_symbol_API(
            symbol, startDate, endDate, limit, coinHeaders)
        return jsonify(res.json())
    except ValueError:
        return jsonify({"message": "Error"})


if __name__ == '__main__':
    app.run(debug=True)
