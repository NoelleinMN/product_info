"""Server for myRetail RESTful API"""

from flask import Flask
import urllib.request
from urllib.request import urlopen
import json

import os


app = Flask(__name__)


API_KEY = os.environ['REDSKY_KEY']


@app.route("/")
def welcome():
    return "<h1>Landing page for myRetail RESTful API</h1>"

@app.route("/products")
def products_landing():
    return "<p>Getting warmer. Why not try a product ID?</p>"

@app.route("/products/test")
def get_redsky_info():
    url = "https://redsky-uat.perf.target.com/redsky_aggregations/v1/redsky/case_study_v1?key={}&tcin=84836363".format(API_KEY)

    response = urllib.request.urlopen(url)
    data = response.read()

    return data


if __name__ == '__main__':
    app.run(debug=True)
