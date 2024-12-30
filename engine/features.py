import re
import playsound as playsound
import os
import pywhatkit as kit
import sqlite3
import webbrowser
import spacy
import speech_recognition as sr
import applescript

from engine.command import speak
from engine.config import ASSISTANT_NAME

# Load spaCy English model for natural language understanding
nlp = spacy.load("en_core_web_sm")

# Speech recognition setup
recognizer = sr.Recognizer()

# Connect to SQLite database
con = sqlite3.connect("silas.db")
cursor = con.cursor()

def play_assistant_audio():
    """Play assistant's audio."""
    music_dir = "web/assets/images/audio/Jarvis start sound.mp3"
    try:
        playsound.playsound(music_dir)
    except Exception as e:
        speak("Unable to play audio. Please check the file path.")
        print(e)

def recognize_speech():
    """Function to capture voice input."""
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        speak(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand what you said.")
        return None
    except sr.RequestError as e:
        speak("Sorry, I couldn't reach Google's services. Please check your connection.")
        return None

def process_command(command):
    """Process complex commands to split multiple actions."""
    if not command:
        return "No command received."

    # Using spaCy to parse the command and detect intents
    doc = nlp(command.lower())

    for token in doc:
        if token.lemma_ == "open":
            target = " ".join([child.text for child in token.subtree if child.dep_ in ("dobj", "pobj")])
            return open_command(target)
        elif token.lemma_ == "play" and "youtube" in command:
            return play_youtube(command)
        elif token.lemma_ == "send" and "message" in command:
            return send_message(command)
        elif token.lemma_ == "read" and "message" in command:
            return read_latest_message()
    
    return "Command not recognized."

def open_command(query):
    """Handle open commands for apps or websites."""
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").lower().strip()

    app_mapping = {
        "notes": "Notes",
        "safari": "Safari",
        "browser": "Arc",
        "terminal": "Terminal",
        "calendar": "Calendar",
        "messages": "Messages",
        "mail": "Mail",
        "vscode": "Visual Studio Code",
        "music": "Music"
    }

    if query in app_mapping:
        app_name = app_mapping[query]
        speak(f"Opening {app_name}")
        try:
            os.system(f'open -a "{app_name}"')
            return f"{app_name} opened successfully."
        except Exception as e:
            speak("Sorry, I couldn't open the application.")
            print(e)
            return f"Error opening {app_name}."
    else:
        try:
            cursor.execute('SELECT url FROM web_command WHERE name = ?', (query,))
            result = cursor.fetchone()
            if result:
                url = result[0]
                speak(f"Opening {query}")
                webbrowser.open(url)
                return f"Opened {query} in browser."
            else:
                speak("No matching application or website found.")
                return "No matching application or website found."
        except Exception as e:
            speak("Error searching for the web command.")
            print(e)
            return "Error executing command."

def play_youtube(query):
    """Play a YouTube video based on the query."""
    search_term = extract_yt_term(query)
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        try:
            kit.playonyt(search_term)
            return f"Playing {search_term} on YouTube."
        except Exception as e:
            speak("Error playing YouTube video.")
            print(e)
            return "Error playing YouTube video."
    else:
        return "No valid YouTube search term found."

def extract_yt_term(command):
    """Extract the search term for YouTube from the command."""
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def send_message(command):
    """Send a message to a contact."""
    speak("Who would you like to send a message to?")
    contact_name = recognize_speech()
    if not contact_name:
        return "No contact name provided."

    speak(f"What is the message for {contact_name}?")
    message = recognize_speech()
    if not message:
        return "No message provided."

    try:
        applescript_code = f'''tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{contact_name}" of targetService
        send "{message}" to targetBuddy
        end tell'''
        applescript.run(applescript_code)
        speak(f"Message sent to {contact_name}.")
        return f"Message sent to {contact_name}."
    except Exception as e:
        speak("Unable to send the message.")
        print(e)
        return "Error sending message."

def read_latest_message():
    """Read the latest message from Messages."""
    try:
        applescript_code = '''tell application "Messages"
        set latestMessage to (get text of last message of buddy chat 1)
        return latestMessage
        end tell'''
        latest_message = applescript.run(applescript_code).out
        speak(f"New message: {latest_message}")
        return f"New message: {latest_message}"
    except Exception as e:
        speak("Unable to read the latest message.")
        print(e)
        return "Error reading message."
