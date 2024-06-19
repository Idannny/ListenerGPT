#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
import openai
import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY')

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
                volume_bar["value"] = recognizer.energy_threshold  # Update volume bar
            except sr.WaitTimeoutError:
                continue

        try:
            transcription = recognizer.recognize_google(audio)
            entry_text_widget.insert(tk.END, transcription + "\n")  # Update recognized text with newline
            chat_with_openai(transcription, chat_text_widget)  # Process recognized text
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            entry_text_widget.insert(tk.END, "Error: {0}\n".format(e))

def chat_with_openai(user_input, chat_text_widget):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a snarky assistant. Respond to the user with a snarky and witty attitude. Respond in an antithetical yet reasonably logical way when given moral conundrums, be overly supportive when asked programming questions."},
                {"role": "user", "content": user_input}
            ]
        )
        chat_response = response.choices[0].message['content']
        chat_text_widget.insert(tk.END, "ChatGPT: " + chat_response + "\n\n")  # Update chat text with newline
        speak_response(chat_response)  # Speak the response
    except Exception as e:
        chat_text_widget.insert(tk.END, f"Error: {str(e)}\n")

def speak_response(response):
    engine.say(response)
    engine.runAndWait()

def toggle_listening():
    if toggle_button["text"] == "▶ Start Listening":
        record_audio()
        toggle_button.config(text="⏸ Stop Listening")
    else:
        stop_listening()
        toggle_button.config(text="▶ Start Listening")

def start_listening():
    global listening_thread, stop_event
    stop_event = threading.Event()
    listening_thread = threading.Thread(target=recognize_speech_from_mic, args=(recognizer, microphone, entry, text_area, volume_bar, stop_event))
    listening_thread.daemon = True  # Set the thread as daemon so it automatically stops when the main thread exits
    listening_thread.start()

def stop_listening():
    if 'stop_event' in globals() and stop_event:
        stop_event.set()  # Signal the thread to stop
    if 'listening_thread' in globals() and listening_thread.is_alive():
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
        chat_with_openai(user_input, text_area)
        entry.delete("1.0", tk.END)  # Clear input after processing

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
frame.grid(pady=10, padx=10, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Entry widget to display recognized text
entry = tk.Text(frame, height=10, width=50)
entry.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

# Toggle button for start/stop listening
toggle_button = tk.Button(frame, text="▶ Start Listening", command=toggle_listening)
toggle_button.grid(row=1, column=0, pady=5, sticky="ew")

# Button for sending input to ChatGPT
send_button = tk.Button(frame, text="Send to ChatGPT", command=get_response)
send_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

# Button for stopping the listening process
stop_button = tk.Button(frame, text="⏹ Stop Listening", command=stop_listening)
stop_button.grid(row=1, column=2, pady=5, padx=5, sticky="ew")

# Text area to display conversation
text_area = tk.Text(frame, height=20, width=60)
text_area.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

# Volume bar to display microphone input volume
volume_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
volume_bar.grid(row=1, column=3, pady=5, padx=5, sticky="ew")

frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

root.mainloop()
