from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ThingSpeak API URL
API_URL = "https://api.thingspeak.com/channels/2389456/feeds.json"

# Your ThingSpeak channel ID and API key
CHANNEL_ID = "2389456"
API_KEY = "DM90K26MXMRO6D9U"

# Route to retrieve data from ThingSpeak
@app.route('/get_data')
def get_data():
    try:
        # Construct the API URL
        url = API_URL.format(channel_id=CHANNEL_ID)
        # Add API key and limit to 1 entry
        params = {'api_key': API_KEY, 'results': 1}
        
        # Make GET request to ThingSpeak
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status
        
        # Extract data from response
        data = response.json()['feeds'][0]
        # Extract field1 data (assuming the string data is in field1)
        string_data = data['field1']
        
        # Extract digits from the string_data until *
        digits = ''
        for char in reversed(string_data):
            if char == '*':
                break
            if char.isdigit():
                digits = char + digits
        
        return jsonify({'digits': digits})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
