# -*- coding: utf-8 -*-

"""Server for myRetail RESTful API"""

from flask import (Flask, jsonify, abort, make_response, render_template, request, redirect)
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
import json
# from bson.json_util import dumps
import os
import requests


app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False
app.config['JSON_AS_ASCII'] = False

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

#@app.route("/products/price/<int:id>")
def get_price(id):
    price = product_price.find_one({'_id': id})

    if price is not None:
        return price['current_price']

    else:
        json = jsonify(message=("Price information for {} is not available".format(id)))
        response = make_response(json, 400)
        abort(response)

@app.route("/products/<int:id>")
def get_redsky_info(id):
    url = "https://redsky-uat.perf.target.com/redsky_aggregations/v1/redsky/case_study_v1?key={}&tcin={}".format(API_KEY, id)

    response = requests.get(url)
    data = response.json()

    try:
        product_id = data['data']['product']['tcin']
    except KeyError:
        json = jsonify(message=("No product found with tcin {}".format(id)))
        response = make_response(json, 400)
        abort(response)

    else:

        product_id = data['data']['product']['tcin']
        pattern = "#38;"
        name = data['data']['product']['item']['product_description']['title'].replace(pattern,"")

        product = {
            "id": product_id,
            "name": name,
            "current_price": get_price(id)
        }

        return product

@app.errorhandler(HTTPException)
def handle_exception(err):
    return jsonify({"message": err.description}), err.code

if __name__ == '__main__':
    app.run(debug=True)
