# Challenge
Build a RESTful products API, which will aggregate product data from multiple sources and return it as JSON to the caller.

# Tech Stack
- Python
- MongoDB
- Flask
- Tests with unittest and mongomock

# Requirements / Features

Users can:
- Retrieve product and price information by product ID (HTTP GET request at /products/{id} ) delivered via JSON
  - product information comes from an external API
  - price information comes from NoSQL data store
- Update price by product ID within the data store (HTTP PUT request at /products/{id} )
  - send price update to the specific id endpoint
  - error handling if endpoint is invalid
  - success message if valid enpoint, and price is updated

# How to use the API

Please follow these steps to run this API on your local device.

Initial setup:

1. Install [Python 3.10](https://www.python.org/downloads/), [MongoDB 5.0](https://www.mongodb.com/docs/manual/installation/), [pip](https://pip.pypa.io/en/stable/installation/) and [Virtualenv](https://pypi.org/project/virtualenv/) in your project directory (or use global installations and paths, if you prefer) using the package manager of your choice. [Homebrew](https://brew.sh/) is highly recommended for macOS or Linux users.
2. Clone repository: `git clone https://github.com/NoelleinMN/product_info.git`
3. Create a virtual environment: `virtualenv env`
4. Activate the Virtualenv via the command line: `source env/bin/activate` (Note that you need only type `deactivate` to exit the virtualenv when you are done with your session)
5. Install dependencies: `pip install -r requirements.txt`
6. Save the provided API key for the challenge to your local environemnt with `export API_KEY=<put_key_here>`
7. Source your keys from the os by adding these two lines to your code: `import os` and `API_KEY = os.environ['API_KEY']`
8. Run the app from the command line: `python3 server.py`
9. You can now navigate to 'localhost:5000/' to access the API!


# How to test the API

The test suite can be run from the command line with `python3 test.py`

Manual cURL checks are structured as follows:
`curl -H "Content-Type: application/json" -X GET http://localhost:5000/products/13860428` (could add the -i flag for additional information/output)

cURL for PUT method (to update price in the data store and API) is structured as follows:
`curl -X PUT --header 'Content-Type: application/json' -d '{"current_price.value": 9.99}' http://localhost:5000/products/13860428`
