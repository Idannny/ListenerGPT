import pyttsx3

class SpeechAgent:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak_text(self, text):
        """Converts text to speech and plays it."""
        self.engine.say(text)
        self.engine.runAndWait()
