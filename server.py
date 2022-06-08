"""Server for myRetail RESTful API"""

from flask import Flask
from pymongo import MongoClient
import urllib.request
from urllib.request import urlopen
import json
from bson.json_util import dumps
import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.products
product_price = db.product_price

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

@app.route("/products/price")
def get_price():
    price = product_price.find_one()
    price_payload = dumps(price)

    return price_payload

if __name__ == '__main__':
    app.run(debug=True)
