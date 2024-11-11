from app.agents.file_agent import FileAgent
from app.agents.image_agent import ImageAgent
from app.agents.api_agent import ApiAgent
from app.agents.speech_agent import SpeechAgent

def start_assistant():
    # Initialize the agents
    file_agent = FileAgent()
    image_agent = ImageAgent()
    api_agent = ApiAgent()
    speech_agent = SpeechAgent()

    # Example of how agents might interact based on user input
    while True:
        user_input = input("How can I assist you? ")

        if "upload file" in user_input:
            # Ask for file path to upload
            source_path = input("Please provide the full path of the file to upload: ")
            file_agent.upload_file(source_path)
        elif "recognize object" in user_input:
            image_agent.recognize_objects()
        elif "weather" in user_input:
            # Optionally, ask for city name
            city = input("Enter the city for weather information: ")
            api_agent.get_weather(city)
        elif "speak" in user_input:
            speech_agent.speak_text("Hello, how can I help you today?")
        elif user_input.lower() == "exit":
            print("Goodbye!")
            break
        else:
            print("Sorry, I didn't understand that. Please try again.")
