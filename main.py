import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from engine.features import *
from engine.command import *

# Initialize Flask app
app = Flask(__name__, static_folder="web")
CORS(app)  # Allow CORS for frontend-backend communication

# API endpoint to handle user input
@app.route('/api/message', methods=['POST'])
def process_message():
    data = request.json  # Get JSON data from frontend
    user_message = data.get("message", "")
    # Example logic: process the user input
    response_message = f"You said: {user_message}"  # Replace this with your actual logic
    return jsonify({"response": response_message})

# API endpoint to play audio
@app.route('/api/audio', methods=['GET'])
def play_audio():
    # Path to the audio file in the web/assets/images directory
    audio_folder = os.path.join("web", "assets", "images", "audio")
    audio_filename = "Jarvis start sound.mp3"  # Replace with the actual file name
    return send_from_directory(audio_folder, audio_filename)

# Open the Netlify site in Arc browser
def open_arc_browser():
    time.sleep(2)  # Small delay before opening the browser
    os.system("open -a 'Arc' https://silasai.netlify.app")

# Start the Flask server
if __name__ == "__main__":
    # Step 1: Start the backend server
    open_arc_browser()  # Step 2: Open the Netlify site in Arc browser
    app.run(host="0.0.0.0", port=3000, debug=True)
