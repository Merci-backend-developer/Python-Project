import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Network error. Please try again.")
            return ""

def handle_command(command):
    """Process the command and execute tasks."""
    if "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    elif "weather" in command:
        speak("Please provide your city.")
        city = listen()
        if city:
            get_weather(city)
    elif "open" in command:
        app = command.replace("open", "").strip()
        open_application(app)
    else:
        speak("I didn't understand the command. Please try again.")

def get_weather(city):
    """Fetch weather details."""
    api_key = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp}°C with {description}.")
        else:
            speak("Sorry, I couldn't find the weather for that location.")
    except Exception as e:
        speak("Unable to fetch weather details. Please try again later.")

def open_application(app_name):
    """Open a specified application."""
    app_paths = {
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
    }
    path = app_paths.get(app_name.lower())
    if path:
        os.startfile(path)
        speak(f"Opening {app_name}.")
    else:
        speak(f"I don't know how to open {app_name}.")

if __name__ == "__main__":
    speak("Hello! I am your personal assistant. How can I help you today?")
    while True:
        user_command = listen()
        if "exit" in user_command or "stop" in user_command:
            speak("Goodbye!")
            break
        handle_command(user_command)
