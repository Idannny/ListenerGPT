import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import openai
import os
import python_chess
import python_chess.svg
from io import BytesIO
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Chess board setup
board = python_chess.Board()

def draw_board():
    # Load the board SVG
    board_svg = python_chess.svg.board(board)
    board_image = Image.open(BytesIO(board_svg.encode('utf-8')))
    board_photo = ImageTk.PhotoImage(board_image)
    
    # Display the board on the GUI
    board_label.config(image=board_photo)
    board_label.image = board_photo

def make_move(move):
    if board.is_legal(python_chess.Move.from_uci(move)):
        board.push(python_chess.Move.from_uci(move))
        draw_board()
    else:
        chat_text_widget.insert(tk.END, "Invalid move.\n")

def chat_with_openai(user_input, chat_text_widget):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a snarky assistant. Respond to the user with a snarky and witty attitude."},
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

# Setting up the GUI
root = tk.Tk()
root.title("Voice to ChatGPT with Chess")

# Set the icon for the application
icon_path = "icon.png"  # Change to your icon file path
if os.path.exists(icon_path):
    root.iconphoto(False, tk.PhotoImage(file=icon_path))

frame = tk.Frame(root)
frame.grid(pady=10, padx=10, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Chess board display
board_frame = tk.Frame(frame)
board_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")
board_label = tk.Label(board_frame)
board_label.grid(row=0, column=0, sticky="nsew")
draw_board()

# Entry widget to display recognized text
entry = tk.Text(frame, height=10, width=50)
entry.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

# Button for sending input to ChatGPT
send_button = tk.Button(frame, text="Send to ChatGPT", command=lambda: chat_with_openai(entry.get("1.0", tk.END).strip(), text_area))
send_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

# Text area to display conversation
text_area = tk.Text(frame, height=20, width=60)
text_area.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

root.mainloop()
