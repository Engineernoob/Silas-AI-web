import pyttsx3
import speech_recognition as sr
import eel
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

@eel.expose
def takeCommand():
    """Captures voice input from the user and converts it to text."""
    recognizer = sr.Recognizer()
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        with sr.Microphone() as source:
            speak("Listening...")
            print("Listening...")
            eel.DisplayMessage("Listening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, 10, 6)

        try:
            speak("Recognizing...")
            print("Recognizing...")
            eel.DisplayMessage("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-us")
            print(f"User said: {query}")
            eel.DisplayMessage(query)
            time.sleep(2)
            eel.ShowHood()
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

@eel.expose
def allCommands():
    """Processes user commands based on the speech input."""
    query = ""
    while not query:
        query = takeCommand()

    # Process the command using spaCy to identify different intents
    doc = nlp(query)

    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "youtube" in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    elif "reply" in query:
        from engine.features import reply_to_contact
        reply_to_contact(query)
    elif "shut down" in query or "restart" in query or "log out" in query:
        controlSystem(query)
    elif "increase volume" in query or "decrease volume" in query:
        controlVolume(query)
    elif "increase brightness" in query or "decrease brightness" in query:
        controlBrightness(query)
    elif "search" in query or "define" in query:
        getDefinition(query)
    elif "send message" in query or "reply to message" in query:
        sendMessage(query)
    elif "read message" in query:
        readLatestMessage()
    else:
        # Handling more actions and general responses
        if not respondToGreeting(query):
            handled = False
            for token in doc:
                if token.lemma_ == "open":
                    from engine.features import openCommand
                    # Extract the phrase to open
                    target = " ".join([child.text for child in token.subtree if child.dep_ in ("dobj", "pobj")])
                    openCommand(target)
                    handled = True
                elif token.lemma_ == "play" and "youtube" in query:
                    from engine.features import PlayYoutube
                    PlayYoutube(query)
                    handled = True
                elif token.lemma_ == "reply":
                    from engine.features import reply_to_contact
                    reply_to_contact(query)
                    handled = True
            if not handled:
                speak("I can't run that command, please try again with something else.")

def respondToGreeting(query):
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

def controlSystem(action):
    if "shut down" in action:
        speak("Shutting down the computer.")
        os.system("shutdown now")
    elif "restart" in action:
        speak("Restarting the computer.")
        os.system("shutdown -r now")
    elif "log out" in action:
        speak("Logging out.")
        os.system("osascript -e 'tell application \"System Events\" to log out'")

def controlVolume(action):
    if "increase volume" in action:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        speak("Increasing the volume.")
    elif "decrease volume" in action:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        speak("Decreasing the volume.")

def controlBrightness(action):
    if "increase brightness" in action:
        os.system("brightness +0.1")  # Requires `brightness` tool for macOS
        speak("Increasing brightness.")
    elif "decrease brightness" in action:
        os.system("brightness -0.1")
        speak("Decreasing brightness.")

def getDefinition(query):
    query = query.replace("search", "").replace("define", "").strip()
    try:
        definition = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia: {definition}")
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results for this query. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find information on that topic.")

def sendMessage(query):
    speak("Who would you like to send a message to?")
    contact_name = takeCommand()
    speak(f"What is the message for {contact_name}?")
    message = takeCommand()

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
        response = takeCommand()
        if "yes" in response:
            speak("What would you like to say?")
            reply_message = takeCommand()
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