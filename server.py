"""Server for myRetail RESTful API"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return "<h1>Landing page for myRetail RESTful API</h1>"

@app.route("/products")
def products_landing():
    return "<p>Getting warmer. Why not try a product ID?</p>"

@app.route("/products/<id>")
def redsky_call():
    pass


if __name__ == '__main__':
    app.run(debug=True)

