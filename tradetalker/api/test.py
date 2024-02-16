import json

def get_json_data():
    data = {
        'message': "Welcome to the TradeTalker API!",
        'data': [
            "Article 1",
            "Article 2",
            "Article 3"
        ]
    }
    return json.dumps(data)