import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import sys
import sv_ttk

r = sr.Recognizer()

# Default Settings
recording_time = 5
exit_key = 'q'
filename = "recorded_speech.txt"

def speech_to_text(duration):
    with sr.Microphone() as source:
        print("Listening...")

        r.adjust_for_ambient_noise(source)

        audio = r.record(source, duration=duration)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print("Sorry, an error occurred during speech recognition:", str(e))


def start_capture():
    global recording_time, filename

    recording_duration = recording_time
    result = speech_to_text(recording_duration)
    if result:
        print("You said:", result)
        save_to_file(result, filename)

def save_to_file(text, filename):
    with open(filename, 'a') as file:
        file.write(text + "\n\n")
    print("Recorded speech saved to", filename)

def update_recording_time():
    global recording_time
    recording_time = int(recording_time_entry.get())
    print("Recording time updated to", recording_time)

def update_filename():
    global filename
    filename = filename_entry.get()
    print("Output file name updated to", filename)

def exit_program():
    sys.exit(0)

root = tk.Tk()
root.title("Speech Recorder Settings")

recording_time_label = ttk.Label(root, text="Recording time (sec):")
recording_time_entry = ttk.Entry(root, width=10, justify="center")
recording_time_entry.insert(0, recording_time)
recording_time_button = ttk.Button(root, text="Update", command=update_recording_time)

filename_label = ttk.Label(root, text="Output file name:")
filename_entry = ttk.Entry(root, width=20, justify="center")
filename_entry.insert(0, filename)
filename_button = ttk.Button(root, text="Update", command=update_filename)

start_button = ttk.Button(root, text="Start Capture", command=start_capture)
exit_button = ttk.Button(root, text="Exit", command=exit_program)

recording_time_label.grid(row=0, column=0, padx=10, pady=5)
recording_time_entry.grid(row=0, column=1, padx=10, pady=5)
recording_time_button.grid(row=0, column=2, padx=10, pady=5)

filename_label.grid(row=1, column=0, padx=10, pady=5)
filename_entry.grid(row=1, column=1, padx=10, pady=5)
filename_button.grid(row=1, column=2, padx=10, pady=5)

start_button.grid(row=2, column=0, columnspan=3, padx=50, pady=10)
exit_button.grid(row=3, column=0, columnspan=3, padx=50, pady=10)

sv_ttk.set_theme("dark")

root.mainloop()