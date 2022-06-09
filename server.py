"""Server for myRetail RESTful API"""

# from flask import Flask
from pymongo import MongoClient
# import urllib.request
# from urllib.request import urlopen
import json
from bson.json_util import dumps
import os

from flask import (Flask, jsonify, render_template, request, flash, session,
                   redirect)
import requests


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.products
product_price = db.product_price

API_KEY = os.environ['REDSKY_KEY']


@app.route("/")
def welcome():
    return "<h3>Landing page for myRetail RESTful API</h3>"

@app.route("/products")
def products_landing():
    return "<p>Getting warmer. Why not try a product ID?</p>"

@app.route("/products/<id>")
def get_redsky_info(id):
    url = "https://redsky-uat.perf.target.com/redsky_aggregations/v1/redsky/case_study_v1?key={}&tcin={}".format(API_KEY, id)

    response = requests.get(url)
    data = response.json()
    id = int(data['data']['product']['tcin'])
    name = data['data']['product']['item']['product_description']['title']
    product = {
        "id": id,
        "name": name
    }

    return json.dumps(product)


    # response = urllib.request.urlopen(url)
    # data = response.read()

    # return data

@app.route("/products/price")
def get_price():
    price = product_price.find_one()
    price_payload = dumps(price)

    return price_payload

if __name__ == '__main__':
    app.run(debug=True)
