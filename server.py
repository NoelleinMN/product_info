# -*- coding: utf-8 -*-

"""Server for myRetail RESTful API"""

from flask import (Flask, jsonify, abort, make_response, request)
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
import requests
from flask_httpauth import HTTPBasicAuth
import json
import os


app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False
app.config['JSON_AS_ASCII'] = False
auth = HTTPBasicAuth()

client = MongoClient('localhost', 27017)
db = client.products
product_price = db.product_price

API_KEY = os.environ['REDSKY_KEY']
LOGIN_ID = os.environ['LOGIN']
PUT_PWD = os.environ['LOGIN_PWD']



@app.route("/")
def welcome():
    return "<h3>Landing page for myRetail RESTful API</h3>"

@app.route("/products")
def products_landing():
    return "<p>Getting warmer. Why not try a product ID?</p>"

@app.route("/products/<int:id>", methods=["GET"])
def get_redsky_info(id):
    """Get info from API, parse, retrieve data from collection, compile into JSON output"""

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
            "id": int(product_id),
            "name": name,
            "current_price": get_price(id)
        }

        return product

@app.route("/products/<int:id>", methods=["PUT"])
@auth.login_required
def update_price_info(id):
    """Get info from PUT request, parse, confirm and update data in collection"""

    info = request.get_json()
    new_price = info['current_price.value']
    product_price.update_one({'_id':id}, {"$set": { "current_price.value" : new_price}})
    confirm_new_price = product_price.find_one({'_id': id})

    if confirm_new_price is not None:

        final_price = confirm_new_price['current_price']['value']

        json = jsonify(message=("Price information for {} has been updated to {}".format(id, final_price)))
        response = make_response(json, 200)

        return response

    else:
        json = jsonify(message=("The price for item {} cannot be updated".format(id)))
        response = make_response(json, 400)
        abort(response)

@app.errorhandler(HTTPException)
def handle_exception(err):
    """JSONify standard error messages"""

    return jsonify({"status_code": err.code, "message": err.description})


def get_price(id):
    """Helper function for getting product information from the collection"""

    price = product_price.find_one({'_id': id})

    if price is not None:
        return price['current_price']

    else:
        json = jsonify(message=("Price information for {} is not available".format(id)))
        response = make_response(json, 400)
        abort(response)

@auth.get_password
def get_password(username):
    if username == LOGIN_ID:
        return PUT_PWD
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.run(debug=True)
