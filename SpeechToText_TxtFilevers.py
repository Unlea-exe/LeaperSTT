import speech_recognition as sr
import keyboard
import time

# Create a recognizer object
r = sr.Recognizer()

# Function to convert speech to text
def speech_to_text(duration):
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise levels
        r.adjust_for_ambient_noise(source)

        # Record audio for the specified duration
        audio = r.record(source, duration=duration)

    try:
        # Use Google Speech Recognition to transcribe the audio
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print("Sorry, an error occurred during speech recognition:", str(e))

# Function to start capturing speech on key press
def start_capture(event):
    if event.name == 'k':
        recording_duration = 5  # Specify the recording duration in seconds
        result = speech_to_text(recording_duration)
        if result:
            print("You said:", result)
            save_to_file(result)

# Function to save text to a file
def save_to_file(text):
    filename = "recorded_speech.txt"
    with open(filename, 'a') as file:
        file.write(text) #If you want to not delete the existing line replace this line with file.write(text + "\n\n")
    print("Recorded speech saved to", filename)

# Register the key press event
keyboard.on_press(start_capture)

# Keep the program running until 'q' key is pressed
keyboard.wait('q')
