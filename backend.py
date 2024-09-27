import os
import requests
from flask import Flask, jsonify, render_template, send_from_directory
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from a .env file

app = Flask(__name__, static_folder='static')

# Your CricAPI key
API_KEY = os.getenv('API_KEY')

# CricAPI endpoint for live matches
URL = f'https://api.cricapi.com/v1/matches?apikey={API_KEY}'

def get_live_matches():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' not in data:
            return "No match data available."
        
        matches = data['data']
        
        live_matches = [match for match in matches if match.get('status') == 'live']

        if not live_matches:
            return "No live matches at the moment."
        
        live_data = []
        
        for match in live_matches:
            match_info = {
                "team-1": match.get("teams", [])[0] if match.get("teams") else "Unknown",
                "team-2": match.get("teams", [])[1] if len(match.get("teams", [])) > 1 else "Unknown",
                "score": match.get("score", "No score available"),
                "type": match.get("matchType", "Unknown"),
                "status": match.get("status", "Unknown")
            }
            live_data.append(match_info)

        return live_data

    except requests.exceptions.RequestException as e:
        return f"Error fetching data from CricAPI: {e}"

@app.route('/api/live-scores', methods=['GET'])
def live_scores():
    scores = get_live_matches()
    return jsonify(scores)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/test')
def test():
    return "Backend is working!"


if __name__ == '__main__':
    app.run(debug=True)

