# utils.py
import pyttsx3
import eel

def speak(text):
    """Converts text to speech and displays it using eel."""
    engine = pyttsx3.init('nsss')
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[14].id)  # Adjust this index if necessary for voice selection
    engine.setProperty("rate", 175)
    eel.DisplayMessage(text)  # Display the message in the UI
    engine.say(text)
    engine.runAndWait()
