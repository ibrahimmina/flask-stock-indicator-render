from flask import Flask
import yfinance as yf
import datetime as dt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/about')
def about():

    return yf.download("AAPL", start="2023-01-01", end="2023-04-30")