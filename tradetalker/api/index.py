import json
from flask import Flask, jsonify
from flask_cors import CORS
from test import get_json_data

app = Flask(__name__)
CORS(app) # Allows backend to communicate with JS frontend

# To view the routes, run 'npm run dev' in the terminal and then
# go to http://127.0.0.1:8080/api/home, for example.

# Example of how to create a route and return JSON data from a function
@app.route('/api/home', methods=['GET'])
def index():
    data = json.loads(get_json_data())
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=8080)