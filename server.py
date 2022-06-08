"""Server for myRetail RESTful API"""

from flask import Flask

app = Flask(__name__)

@app.route("/products")
def welcome():
    return "<h1>Landing page for myRetail RESTful API</h1>"


if __name__ == '__main__':
    app.run(debug=True)

