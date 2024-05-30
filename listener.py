import tkinter as tk
import openai
import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import threading
import random
import time

# Load environment variables from .env file
load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY')

def recognize_speech_from_mic(recognizer, microphone, text_widget):
    """Transcribe speech recorded from `microphone`."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=5)
        
        try:
            transcription = recognizer.recognize_google(audio)
            text_widget.insert(tk.END, transcription + " ")
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            text_widget.insert(tk.END, "Error: {0}\n".format(e))

def start_listening():
    global listening_thread
    listening_thread = threading.Thread(target=recognize_speech_from_mic, args=(recognizer, microphone, entry))
    listening_thread.daemon = True  # Set the thread as daemon so it automatically stops when the main thread exits
    listening_thread.start()

def stop_listening():
    if listening_thread.is_alive():
        listening_thread.join()  # Wait for the listening thread to finish

def record_audio():
    # Automatically select a working microphone
    available_microphones = sr.Microphone.list_microphone_names()
    for i, mic_name in enumerate(available_microphones):
        try:
            global microphone, recognizer
            microphone = sr.Microphone(device_index=i)
            recognizer = sr.Recognizer()
            start_listening()
            return
        except Exception as e:
            pass
    entry.insert(tk.END, "Error: No working microphone found.\n")

def get_response():
    user_input = entry.get("1.0", tk.END).strip()

    if user_input:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            chat_response = response.choices[0].message['content']
            text_area.insert(tk.END, "You: " + user_input + "\n")
            text_area.insert(tk.END, "ChatGPT: " + chat_response + "\n\n")
            entry.delete("1.0", tk.END)
            
            # Speak the response
            engine.say(chat_response)
            engine.runAndWait()
        except Exception as e:
            text_area.insert(tk.END, f"Error: {str(e)}\n")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Setting up the GUI
root = tk.Tk()
root.title("Voice to ChatGPT")

# Set the icon for the application
icon_path = "icon.png"  # Change to your icon file path
if os.path.exists(icon_path):
    root.iconphoto(False, tk.PhotoImage(file=icon_path))

frame = tk.Frame(root)
frame.pack(pady=10)

# Entry widget to display recognized text
entry = tk.Text(frame, height=3, width=50)
entry.pack(pady=10)

# Buttons for recording and sending
record_button = tk.Button(frame, text="Start Listening", command=record_audio)
record_button.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(frame, text="Send to ChatGPT", command=get_response)
send_button.pack(side=tk.LEFT, padx=10)

# Text area to display conversation
text_area = tk.Text(root, height=20, width=60)
text_area.pack(pady=10)

root.mainloop()
