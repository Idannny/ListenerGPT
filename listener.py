import tkinter as tk
import openai
import os
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY')

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was successful
    "error": `None` if no error occurred, otherwise a string containing an error message
    "transcription": `None` if speech could not be transcribed, otherwise the transcribed text
    """
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def record_audio():
    # Get selected microphone index
    mic_index = mic_var.get().split(":")[0]
    try:
        microphone = sr.Microphone(device_index=int(mic_index))
    except ValueError:
        text_area.insert(tk.END, "Error: Please select a valid microphone.\n")
        return

    recognizer = sr.Recognizer()
    response = recognize_speech_from_mic(recognizer, microphone)
    
    if response["success"]:
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, response["transcription"])
    else:
        text_area.insert(tk.END, f"Error: {response['error']}\n")

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
        except Exception as e:
            text_area.insert(tk.END, f"Error: {str(e)}\n")

# Setting up the GUI
root = tk.Tk()
root.title("Voice to ChatGPT")

frame = tk.Frame(root)
frame.pack(pady=10)

# Microphone selection dropdown
mic_var = tk.StringVar(root)
mic_var.set("Select Microphone")
mic_menu = tk.OptionMenu(frame, mic_var, *[f"{i}: {name}" for i, name in enumerate(sr.Microphone.list_microphone_names())])
mic_menu.pack(pady=10)

entry = tk.Text(frame, height=3, width=50)
entry.pack(pady=10)

record_button = tk.Button(frame, text="Record Voice", command=record_audio)
record_button.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(frame, text="Send to ChatGPT", command=get_response)
send_button.pack(side=tk.LEFT, padx=10)

text_area = tk.Text(root, height=20, width=60)
text_area.pack(pady=10)

root.mainloop()
