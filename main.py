import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from engine.features import process_command, play_assistant_audio
from engine.command import all_commands

# Initialize Flask app
app = Flask(__name__, static_folder="web")
CORS(app)  # Allow CORS for frontend-backend communication

@app.route('/api/startup', methods=['GET'])
def startup():
    # Play the assistant's audio during initialization
    play_assistant_audio()
    return jsonify({"message": "Assistant audio played on startup."})

@app.route('/api/message', methods=['POST'])
def process_message():
    data = request.json
    user_message = data.get("message", "")
    response = process_command(user_message)
    return jsonify({"response": response})

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
