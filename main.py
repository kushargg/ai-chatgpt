import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests 
from openai import OpenAI
from gtts import gTTS
import pygame
import os 
#   pip install pocketsphinx

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "4d3071635116454b9ae4b26817e32148"

# Function to speak text
def speak_old(text):
    """Speaks the given text using the text-to-speech engine."""
    if engine is not None:  # Check if engine is initialized successfully
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"Jarvis: {text}")  # Print to console if TTS fails
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')   

    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3") 

    # Set volume (optional)
    pygame.mixer.music.set_volume(0.7) 

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running 
    while pygame.mixer.music.get_busy():
        continue 

    pygame.mixer.music.stop()   
    pygame.mixer.music.unload() 
    os.remove("temp.mp3")
#  Below code is  typing the text  and the answer will get  in speak mode as well as writen formate  

def aiProcess(command):
    """Processes a user command using OpenAI's gpt-4o-mini model."""

    # Replace with your actual OpenAI API key (remove placeholder)
    api_key = "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"

    if not api_key:
        print("Error: OpenAI API key not set. Please set the OPENAI_API_KEY environment variable or provide your key here.")
        return None  # Indicate error or provide a default message

    client = OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud give short responsive please"},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as err:
        return f"An error occurred: {err}"

if __name__ == "__main__":
    while True:
        user_command = input("speak: ")
        if user_command.lower() in ["exit", "quit", "bye"]:
            speak("Goodbye!")
            break

        output = aiProcess(user_command)
        if output and not output.startswith("An error occurred"):
            speak(output)
            print("Jarvis:", output)
        elif output:
            print("Jarvis:", output)
            speak("I encountered an issue. Please check the console for details.")
        else:
            speak("I encountered an issue. Please check the console for details.")
        





def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        
    elif "open linkdin" in c.lower():
        webbrowser.open("https://linkdin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "close facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():    
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=4d3071635116454b9ae4b26817e32148")

        if r.status_code == 200:
            data = r.json()

    # Check if 'articles' key exists in the response
    articles = data.get('articles', [])

    # Loop through the articles and print the headlines
    for article in articles:
        speak(article["title"])
    
   
    else:
        # let openai handle the request 
        output = aiProcess(command)
        speak(output)
        pass

# Main program
if __name__ == "__main__":  # Corrected typo in "__main__"
    speak("Initializing Jarvis....")
    while True:
        # listen for the wake word "Jarvis"


        # obtain audio from the microphone
        r = sr.Recognizer()
        
        
        
        print("recognizing....")

        # recognize speech using sphinx

        try:
            with sr.Microphone() as source:
                print("Listen...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() =="jarvis"):
                speak("ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
       
       
       
       
       
       
       
       
       
        except Exception as e:
            print("Error; {0}".format(e)) 
