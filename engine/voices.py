import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init('nsss')

# Get the list of available voices
voices = engine.getProperty('voices')

# Iterate through the voices to print only non-Neuter voices (i.e., Male or Female)
filtered_voices = []
for index, voice in enumerate(voices):
    if voice.gender != 'VoiceGenderNeuter':
        filtered_voices.append(voice)
        print(f"Voice {len(filtered_voices) - 1}:")  # Re-index the filtered list
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Gender: {voice.gender}")
        print(f" - Language: {voice.languages}\n")

# Check if there are any voices after filtering
if filtered_voices:
    # Set a specific voice by its index (for example, voice 0)
    engine.setProperty('voice', filtered_voices[7].id)  # Change the index if desired

    # Set the speaking rate if needed
    engine.setProperty('rate', 200)  # Default rate is usually around 200

    # Speak the text
    engine.say("Hello, I am your assistant!")
    engine.runAndWait()
else:
    print("No suitable voices found (excluding neuter).")
