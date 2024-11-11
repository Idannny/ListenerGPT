#!/usr/bin/env python

import customtkinter as ctk  # Import CustomTkinter
import openai
import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import threading
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
# Load environment variables from .env file
load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function for recognizing speech and handling chat
def recognize_speech_from_mic(recognizer, microphone, entry_text_widget, chat_text_widget, volume_bar, stop_event):
    """Transcribe speech recorded from `microphone`."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    while not stop_event.is_set():
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                volume_bar.set(recognizer.energy_threshold)  # Update volume bar
            except sr.WaitTimeoutError:
                continue

        try:
            transcription = recognizer.recognize_google(audio)
            entry_text_widget.insert(ctk.END, transcription + "\n")  # Update recognized text with newline
            chat_with_openai(transcription, chat_text_widget)  # Process recognized text
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            entry_text_widget.insert(ctk.END, "Error: {0}\n".format(e))

# Function for ChatGPT response
def chat_with_openai(user_input, chat_text_widget):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a charming, playful, yet snarky assistant..."},
                {"role": "user", "content": user_input}
            ]
        )
        chat_response = response.choices[0].message['content']
        chat_text_widget.insert(ctk.END, "ChatGPT: " + chat_response + "\n\n")
        speak_response(chat_response)
    except Exception as e:
        chat_text_widget.insert(ctk.END, f"Error: {str(e)}\n")

# Function for text-to-speech response
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# Toggle listening function
def toggle_listening():
    if toggle_button.cget("text") == "▶ Start Listening":
        record_audio()
        toggle_button.configure(text="⏸ Stop Listening")
    else:
        stop_listening()
        toggle_button.configure(text="▶ Start Listening")

# Functions to start/stop listening
def start_listening():
    global listening_thread, stop_event
    stop_event = threading.Event()
    listening_thread = threading.Thread(target=recognize_speech_from_mic, args=(recognizer, microphone, entry, text_area, volume_bar, stop_event))
    listening_thread.daemon = True
    listening_thread.start()

def stop_listening():
    if 'stop_event' in globals() and stop_event:
        stop_event.set()
    if 'listening_thread' in globals() and listening_thread.is_alive():
        listening_thread.join()

# Record audio function with microphone selection
def record_audio():
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
    entry.insert(ctk.END, "Error: No working microphone found.\n")

# Function for ChatGPT response submission
def get_response():
    user_input = entry.get("1.0", ctk.END).strip()

    if user_input:
        chat_with_openai(user_input, text_area)
        entry.delete("1.0", ctk.END)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Setting up CustomTkinter GUI
ctk.set_appearance_mode("Dark")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Voice to ChatGPT")

# Set the icon for the application
icon_path = "media\icon.png"  # Adjust path as needed

if os.path.exists(icon_path):
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)  # Convert to Tkinter-compatible PhotoImage
    root.iconphoto(False, icon_photo)  # 

frame = ctk.CTkFrame(root)
frame.grid(pady=10, padx=10, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Entry widget to display recognized text
entry = ctk.CTkTextbox(frame, height=150, width=400)
entry.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

# Toggle button for start/stop listening
toggle_button = ctk.CTkButton(frame, text="▶ Start Listening", command=toggle_listening)
toggle_button.grid(row=1, column=0, pady=5, sticky="ew")

# Button for sending input to ChatGPT
send_button = ctk.CTkButton(frame, text="Send to ChatGPT", command=get_response)
send_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

# Button for stopping the listening process
stop_button = ctk.CTkButton(frame, text="⏹ Stop Listening", command=stop_listening)
stop_button.grid(row=1, column=2, pady=5, padx=5, sticky="ew")

# Text area to display conversation
text_area = ctk.CTkTextbox(frame, height=300, width=600)
text_area.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

# Volume bar to display microphone input volume
volume_bar = ctk.CTkProgressBar(frame, orientation="horizontal", mode="determinate", width=200)
volume_bar.grid(row=1, column=3, pady=5, padx=5, sticky="ew")

frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

root.mainloop()
