from flask import Flask
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/about')
def about():
    return yf.download("AAPL", "2023-01-01", "2023-01-02")