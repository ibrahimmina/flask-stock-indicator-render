from flask import Flask
import yfinance as yf
import datetime as dt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/about')
def about():
    startdate = dt.datetime.strptime("2023-01-01", "%Y-%m-%d").date()
    enddate = dt.datetime.strptime("2023-01-02", "%Y-%m-%d").date()

    return yf.download("AAPL", start=startdate, end=enddate, interval="1d")