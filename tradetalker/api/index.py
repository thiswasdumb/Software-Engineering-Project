from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows backend to communicate with JS frontend

# Example of how to create a route and return JSON data
@app.route('/api/home', methods=['GET'])
def index():
    return jsonify({
        'message': "Welcome to the TradeTalker API!",
        'data': [
            "Article 1",
            "Article 2",
            "Article 3"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)