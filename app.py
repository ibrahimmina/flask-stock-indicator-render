from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length

from flask import request
from flask import jsonify
import yfinance as yf
import requests

from data import ACTORS
from modules import get_names, get_actor, get_id


from PIL import Image
import base64
import io

import cv2
import numpy as np



# Importing the pandas library 
# and giving it an alias 'pd'
import pandas as pd
 
# Importing the pandas_ta library 
# and giving it an alias 'ta'
import pandas_ta as ta


app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


class UploadForm(FlaskForm):
    image = FileField()
    animal = SelectField(u'See through this animal eyes', choices=['elephant', 'cat', 'dog'])
    submit = SubmitField('Submit')
    


def download_stock_data(symbol, start_date, end_date):
    return yf.download(symbol, start=start_date, end=end_date)

def calculate_bollinger_bands(stock_data, length=20):
    stock_data.ta.bbands(close="Close", length=length, append=True)
    return stock_data[['BBM_{}_2.0'.format(length), 'BBU_{}_2.0'.format(length), 'BBL_{}_2.0'.format(length)]]

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    message = ""
    if form.validate_on_submit():
        name = form.animal.data
        image_data = request.files['image'].stream
        img = Image.open(image_data)
        image_data = np.asarray(img)
        image_gray=cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY )
        
        # encode
        is_success, buffer = cv2.imencode(".jpg", image_gray)
        io_buf = io.BytesIO(buffer)

        # Convert to base64 encoding and show start of data
        jpg_as_text = base64.b64encode(buffer)

        # Convert back to binary
        jpg_original = base64.b64decode(jpg_as_text)

      

        return render_template('animal.html', name=name, photo=jpg_as_text.decode('utf-8'))
    return render_template('index.html', form=form, message=message)


@app.route('/animal/<name>')
def animal(name):

    return render_template('animal.html', name=name)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500