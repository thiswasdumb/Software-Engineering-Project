"""Contains the Flask application to send data to the TradeTalker frontend."""

import os

from flask import Flask, Response, jsonify, redirect, url_for
from flask_cors import CORS
from werkzeug.wrappers import Response as BaseResponse

from database.db import Database

app = Flask(__name__)
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "TradeTalkerDB"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
db = Database(app)  # Initializes the database connection
CORS(app)  # Allows backend to communicate with JS frontend

# To view the routes, run 'npm run dev' in the terminal and then
# go to http://127.0.0.1:8080/api/home, for example.


# Example of how to create a route and return JSON data from a function
@app.route("/api/example", methods=["GET"])
def example() -> Response:
    """Returns example SQL query."""
    return jsonify(db.user_select_all())


# Redirecting to another route
@app.route("/api/redirect", methods=["GET"])
def red() -> BaseResponse:
    """Redirects to the TradeTalker frontend."""
    return redirect(url_for("home"), code=302)


# Redirecting to a new page
@app.route("/api/home", methods=["GET"])
def home() -> BaseResponse:
    """Returns sample JSON data."""
    return redirect("http://localhost:3000/", code=301)


if __name__ == "__main__":
    app.run(debug=os.environ["ENV"] == "dev", port=8080)
