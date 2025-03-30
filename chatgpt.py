import speech_recognition as sr
import webbrowser
import pyttsx3  # Still used for some fallback
import musicLibrary  # Assuming this contains your music library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import datetime
import wikipedia

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()  # For fallback if gTTS has issues
newsapi_key = "4d3071635116454b9ae4b26817e32148"  # Replace with your actual key
openai_api_key = "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"  # Replace with your actual key
client = OpenAI(api_key=openai_api_key) # Initialize OpenAI client globally


# --- Speech Functions ---
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def speak_fallback(text): # Use pyttsx3 as a backup
    engine.say(text)
    engine.runAndWait()

# --- OpenAI Interaction ---
def ai_process(command):
    try:
        completion = client.chat.completions.create(
            model="gpt-4-0613", # Using gpt-4 is recommended if you have access. If not, keep gpt-3.5-turbo or gpt-3.5-turbo-0613
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis.  Give concise and helpful responses."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as err:
        print(f"OpenAI Error: {err}")  # Print error for debugging
        return "I'm having trouble connecting to the AI. Please try again later."  # User-friendly message

# --- Jarvis Commands ---
def process_command(command):
    command = command.lower()  # Process commands in lowercase

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
    elif "play" in command:  # More flexible "play" command
        try:
            song = command.replace("play", "").strip()  # Extract song name
            link = musicLibrary.music.get(song)  # Use .get() to handle missing keys safely
            if link:
                webbrowser.open(link)
            else:
                speak("I couldn't find that song in your library.")
        except Exception as e:
            speak("There was a problem playing the song.")
            print(f"Music Error: {e}")

    elif "news" in command:
        try:
            res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi_key}")  # Use f-string
            res.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = res.json()
            articles = data.get('articles', [])
            if articles:
                for i in range(min(3, len(articles))):  # Speak 3 headlines
                    article = articles[i]
                    speak(f"Headline {i+1}: {article['title']}")
            else:
                speak("I couldn't retrieve the news.")
        except requests.exceptions.RequestException as e:
            speak("There was a problem fetching the news.")
            print(f"News API Error: {e}")

    elif "time" in command:
        now = datetime.datetime.now()
        speak(f"The time is {now.strftime('%I:%M %p')}")  # Format the time

    elif "wikipedia" in command:
        try:
            query = command.replace("wikipedia", "").strip()
            result = wikipedia.summary(query, sentences=2) # Get a short summary
            speak(result)
        except wikipedia.exceptions.PageError:
            speak("I couldn't find that on Wikipedia.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Which one did you mean? " + str(e))
        except Exception as e:
            speak("There was a problem accessing Wikipedia.")
            print(f"Wikipedia Error: {e}")

    else:  # Default to OpenAI for other commands
        ai_response = ai_process(command)
        speak(ai_response)


# --- Main Loop ---
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        with sr.Microphone() as source:
            print("Listening for 'Jarvis'...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3) # Increased timeout
                wake_word = recognizer.recognize_google(audio).lower()
                if "jarvis" in wake_word:  # More flexible wake word detection
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10) # Increased timeout
                        command = recognizer.recognize_google(audio)
                        print("Command:", command) # Print command for debugging
                        process_command(command)

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.WaitTimeoutError:
                print("No speech detected within timeout") # Handle timeout gracefully
            except Exception as e:
                print(f"Main Loop Error: {e}")  # Catch any other errors