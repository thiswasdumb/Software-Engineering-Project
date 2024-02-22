"""Contains the Flask application to send data to the TradeTalker frontend."""

import json
import os

from flask import Flask, Response, jsonify
from flask_cors import CORS

from db import Database
from test_file import get_json_data

app = Flask(__name__)
CORS(app)  # Allows backend to communicate with JS frontend
mysql = Database(app)  # Initializes the database connection

# To view the routes, run 'npm run dev' in the terminal and then
# go to http://127.0.0.1:8080/api/home, for example.


# Example of how to create a route and return JSON data from a function
@app.route("/api/home", methods=["GET"])
def index() -> Response:
    """Returns sample JSON data."""
    data = json.loads(get_json_data())
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=os.environ["ENV"] == "dev", port=8080)
