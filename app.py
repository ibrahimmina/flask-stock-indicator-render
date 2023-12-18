from flask import Flask
from flask import request
from flask import jsonify
import yfinance as yf
import requests

# Importing the pandas library 
# and giving it an alias 'pd'
import pandas as pd
 
# Importing the pandas_ta library 
# and giving it an alias 'ta'
import pandas_ta as ta


app = Flask(__name__)


def download_stock_data(symbol, start_date, end_date):
    return yf.download(symbol, start=start_date, end=end_date)

def calculate_bollinger_bands(stock_data, length=20):
    stock_data.ta.bbands(close="Close", length=length, append=True)
    return stock_data[['BBM_{}_2.0'.format(length), 'BBU_{}_2.0'.format(length), 'BBL_{}_2.0'.format(length)]]

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/about')
def about():

    return jsonify(yf.download("AAPL", start="2023-01-01", end="2023-04-30").tolist())

@app.route('/bollinger', methods=['GET'])
def get_bollinger_bands():
    symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    length = int(request.args.get('length', 20))

    try:
        stock_data = download_stock_data(symbol, start_date, end_date)
        bollinger_data = calculate_bollinger_bands(stock_data, length)

        # Include datetime index  JSON response
        result = {'datetime_index': stock_data.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                  'bollinger_bands': bollinger_data.to_dict(orient='list')}

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})