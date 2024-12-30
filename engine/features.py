import re
import playsound as playsound
import os
import eel
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

@eel.expose
def playAssistantAudio():
    music_dir = "web/assets/images/audio/Jarvis start sound.mp3"
    playsound.playsound(music_dir)

def recognize_speech():
    """Function to capture voice input."""
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        speak(f"You said: {command}")
        process_command(command)
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand what you said.")
    except sr.RequestError as e:
        speak("Sorry, I couldn't reach Google's services. Please check your connection.")

def process_command(command):
    """Process complex commands to split multiple actions."""
    # Using spaCy to parse the command and detect intents
    doc = nlp(command.lower())

    # Loop through all tokens to check for specific actions
    for token in doc:
        if token.lemma_ == "open":
            # Extract the phrase to open
            target = " ".join([child.text for child in token.subtree if child.dep_ in ("dobj", "pobj")])
            openCommand(target)
        elif token.lemma_ == "play":
            # Extract YouTube related commands
            if "youtube" in command:
                PlayYoutube(command)
        elif token.lemma_ == "send" and "message" in command:
            sendMessage(command)
        elif token.lemma_ == "read" and "message" in command:
            readLatestMessage()
        

    # Example for extending more functionality (sending messages, setting reminders)
    # Add more `elif` statements for other intents such as "reply", "set reminder", etc.

def openCommand(query):
    # Clean up the query
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()

    # Mapping to known macOS application names
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

    # Attempt to find the correct application name in the mapping
    if query in app_mapping:
        app_name = app_mapping[query]
        speak(f"Opening {app_name}")
        try:
            os.system(f'open -a "{app_name}"')  # Open the application using macOS command
        except Exception as e:
            speak("Sorry, I couldn't open it. There was an error.")
            print(e)
    else:
        # If the application is not found, check the web_command table for websites
        try:
            cursor.execute('SELECT url FROM web_command WHERE name = ?', (query,))
            result = cursor.fetchone()

            if result:
                # URL found, open it
                url = result[0]
                speak(f"Opening {query}")
                try:
                    webbrowser.open(url)  # Open the URL in the default browser
                except Exception as e:
                    speak("Sorry, I couldn't open the website. There was an error.")
                    print(e)
            else:
                # URL not found, attempt to open directly with open command
                speak(f"Trying to open {query}")
                try:
                    os.system(f'open "{query}"')  # Attempt to open directly
                except Exception as e:
                    speak("Sorry, application or website not found.")
                    print(e)

        except Exception as e:
            speak("Something went wrong while searching for the web command.")
            print(e)

def PlayYoutube(query):
    # Extract the search term from the query
    search_term = extract_yt_term(query)
    
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        try:
            kit.playonyt(search_term)  # Play YouTube video based on search term
        except Exception as e:
            speak("Sorry, I couldn't play the video. There was an error.")
            print(e)
    else:
        speak("Sorry, I couldn't understand the search term.")

def extract_yt_term(command):
    # Define a regular expression pattern to capture the search term
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    
    # If a match is found, return the extracted search term; otherwise, return None
    return match.group(1) if match else None

def sendMessage(command):
    speak("Who would you like to send a message to?")
    contact_name = recognize_speech_input()
    speak(f"What is the message for {contact_name}?")
    message = recognize_speech_input()

    try:
        applescript_code = f'''tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{contact_name}" of targetService
        send "{message}" to targetBuddy
        end tell'''
        applescript.run(applescript_code)
        speak(f"Message sent to {contact_name}.")
    except Exception as e:
        speak("Unable to send the message. Please try again later.")
        print(f"Error: {str(e)}")

def readLatestMessage():
    try:
        applescript_code = '''tell application "Messages"
        set latestMessage to (get text of last message of buddy chat 1)
        return latestMessage
        end tell'''
        latest_message = applescript.run(applescript_code).out
        speak(f"You received a new message: {latest_message}")
        speak("Would you like to reply?")
        response = recognize_speech_input()
        if "yes" in response:
            speak("What would you like to say?")
            reply_message = recognize_speech_input()
            applescript_code_reply = f'''tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy chat 1
            send "{reply_message}" to targetBuddy
            end tell'''
            applescript.run(applescript_code_reply)
            speak("Your reply has been sent.")
    except Exception as e:
        speak("Unable to read the latest message. Please try again later.")
        print(f"Error: {str(e)}")

def recognize_speech_input():
    """Helper function to recognize speech input."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return recognize_speech_input()
    except sr.RequestError as e:
        speak("Sorry, I couldn't reach Google's services. Please check your connection.")
        return ""