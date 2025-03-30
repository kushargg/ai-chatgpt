import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  # Assuming you have this module
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import datetime
import json
import websocket
import cv2  # For face recognition
import numpy as np  # Import numpy explicitly
from PIL import Image
from typing import NoReturn, Optional, Callable, List, Tuple, Any  # For type hinting

# Initialize
recognizer = sr.Recognizer()
pygame.mixer.init()

# Environment variables (best practice)
openai_api_key = os.getenv("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")
newsapi_key = os.getenv("4d3071635116454b9ae4b26817e32148")

if not openai_api_key or not newsapi_key:
    raise ValueError("OPENAI_API_KEY and NEWS_API_KEY environment variables must be set.")

client = OpenAI(api_key=openai_api_key)
# ... (Real-time OpenAI setup - remains the same)

# Face recognition setup
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

try:
    recognizer.read("trainer.yml")
    print("Face recognizer model loaded.")
except FileNotFoundError:
    print("No trainer.yml file found. Train the face recognizer first.")
    # Exit or handle the case where the model isn't available
    exit(1)  # Or raise an exception, or provide a default behavior

# Initialize text-to-speech engine
engine = pyttsx3.init()  # Initialize pyttsx3 engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # You can experiment with voice IDs

def speak(text: str) -> NoReturn:  # Type hinting
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak: {e}")


def greet() -> NoReturn:  # Type hinting
    hour = datetime.datetime.now().hour
    greeting = "Good "
    if 0 <= hour < 12:
        greeting += "Morning!"
    elif 12 <= hour < 18:
        greeting += "Afternoon!"
    else:
        greeting += "Evening!"
    speak(greeting)
    speak("Initializing Jarvis..........")

# ... (Other functions like open_website, play_music, get_news remain the same)


def ai_process(command: str, use_realtime: bool = False) -> str:  # Type hinting
    # ... (Real-time and regular OpenAI API call logic - same as before)
    pass # Placeholder for the code from previous responses

def recognize_face() -> bool:  # Type hinting
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id_, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 60:
                name = "User"  # Replace with your name
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cap.release()
                cv2.destroyAllWindows()
                return True
            else:
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

def listen() -> Optional[str]:  # Type hinting, returns Optional[str]
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Corrected
        audio = recognizer.listen(source)  # Corrected

    try:
        command = recognizer.recognize_google(audio).lower()  # Corrected
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None  # Return None when no command is understood
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# ... (train_recognizer function - remains the same)

if __name__ == "__main__":
    greet()
    while True:
        command = listen()  # No type ignore needed now
        if command:  # Check if command is not None
            if "jarvis" in command:
                speak("Ya.")
                if recognize_face():
                    command = listen()
                    if command: # Check if command is not None
                        # ... (process the command using ai_process, etc.)
                        if "exit" in command.lower() or "quit" in command.lower() or "close" in command.lower():
                            speak("Goodbye!")
                            break
                else:
                    speak("Face not recognized. Please try again.")
        # ... (rest of the main loop)