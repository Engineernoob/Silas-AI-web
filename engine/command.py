import pyttsx3
import speech_recognition as sr
import time
import spacy
import os
import wikipedia
import requests
import json
import applescript

from engine.utils import speak
from engine.config import ASSISTANT_NAME

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

def take_command():
    """Captures voice input from the user and converts it to text."""
    recognizer = sr.Recognizer()
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        with sr.Microphone() as source:
            speak("Listening...")
            print("Listening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)

        try:
            speak("Recognizing...")
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-us")
            print(f"User said: {query}")
            return query.lower()

        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            attempts += 1
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return ""
        except Exception as e:
            speak("Something went wrong. Please try again.")
            print(f"Error: {str(e)}")
            attempts += 1

    speak("I'm sorry, I couldn't understand you after multiple attempts.")
    return ""

def all_commands(query):
    """Processes user commands based on the speech input."""
    if not query:
        return "No command received."

    # Process the command using spaCy to identify different intents
    doc = nlp(query)

    if "open" in query:
        from engine.features import open_command
        return open_command(query)
    elif "youtube" in query:
        from engine.features import play_youtube
        return play_youtube(query)
    elif "reply" in query:
        from engine.features import reply_to_contact
        return reply_to_contact(query)
    elif "shut down" in query or "restart" in query or "log out" in query:
        return control_system(query)
    elif "increase volume" in query or "decrease volume" in query:
        return control_volume(query)
    elif "increase brightness" in query or "decrease brightness" in query:
        return control_brightness(query)
    elif "search" in query or "define" in query:
        return get_definition(query)
    elif "send message" in query or "reply to message" in query:
        return send_message(query)
    elif "read message" in query:
        return read_latest_message()
    else:
        if not respond_to_greeting(query):
            return "Command not recognized. Please try again."

def respond_to_greeting(query):
    """Handles small talk and general greetings."""
    greetings = {
        "how are you": "I'm just a bunch of code, but I am doing great! How can I help you today?",
        "what is your name": f"My name is {ASSISTANT_NAME}, your personal assistant.",
        "who made you": "I was created by Taahirah. She’s amazing!",
        "hello": "Hello! How can I assist you today?",
        "good morning": "Good morning! How can I help make your day easier?",
        "good night": "Good night! Sleep well, and let me know if you need anything before you rest.",
        "thank you": "You're very welcome! I'm always here to help.",
        "what can you do": "I can assist you with tasks like playing music, opening apps, giving you information, and much more!"
    }

    for greeting in greetings:
        if greeting in query:
            speak(greetings[greeting])
            return True
    return False

def control_system(action):
    if "shut down" in action:
        speak("Shutting down the computer.")
        os.system("shutdown now")
        return "Shutting down the system."
    elif "restart" in action:
        speak("Restarting the computer.")
        os.system("shutdown -r now")
        return "Restarting the system."
    elif "log out" in action:
        speak("Logging out.")
        os.system("osascript -e 'tell application \"System Events\" to log out'")
        return "Logging out."

def control_volume(action):
    if "increase volume" in action:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        speak("Increasing the volume.")
        return "Volume increased."
    elif "decrease volume" in action:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        speak("Decreasing the volume.")
        return "Volume decreased."

def control_brightness(action):
    if "increase brightness" in action:
        os.system("brightness +0.1")  # Requires `brightness` tool for macOS
        speak("Increasing brightness.")
        return "Brightness increased."
    elif "decrease brightness" in action:
        os.system("brightness -0.1")
        speak("Decreasing brightness.")
        return "Brightness decreased."

def get_definition(query):
    query = query.replace("search", "").replace("define", "").strip()
    try:
        definition = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia: {definition}")
        return definition
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results for this query. Please be more specific.")
        return "Disambiguation error. Please be more specific."
    except wikipedia.exceptions.PageError:
        speak("I couldn't find information on that topic.")
        return "No information found on the topic."

def send_message(query):
    speak("Who would you like to send a message to?")
    contact_name = take_command()
    speak(f"What is the message for {contact_name}?")
    message = take_command()

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
        speak("Unable to send the message. Please try again later.")
        print(f"Error: {str(e)}")
        return "Error sending message."

def read_latest_message():
    try:
        applescript_code = '''tell application "Messages"
        set latestMessage to (get text of last message of buddy chat 1)
        return latestMessage
        end tell'''
        latest_message = applescript.run(applescript_code).out
        speak(f"You received a new message: {latest_message}")
        return f"New message: {latest_message}"
    except Exception as e:
        speak("Unable to read the latest message. Please try again later.")
        print(f"Error: {str(e)}")
        return "Error reading the latest message."
