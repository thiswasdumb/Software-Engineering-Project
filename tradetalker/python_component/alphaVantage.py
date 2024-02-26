import requests

def get_formatted_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=56RI009LMO7R6F91'
    r = requests.get(url)
    data = r.json()

    time_series = data.get('Time Series (5min)')

    formatted_data = []

    for timestamp, values in time_series.items():
        formatted_data.append({
            'timestamp': timestamp,
            'open': float(values['1. open']),
            'high': float(values['2. high']),
            'low': float(values['3. low']),
            'close': float(values['4. close']),
            'volume': int(values['5. volume']),
        })
    
    return formatted_data

# (replace symbol with the companies and replace the API key with the one we actually got from James)