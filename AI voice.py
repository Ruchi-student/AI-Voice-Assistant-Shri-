import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pygame
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import googletrans
from translate import Translator
from gtts import gTTS
import pyaudio

print('Loading your AI personal assistant - Sri')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

speak("Loading your AI personal assistant Sri")
wishMe()

def translate_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now")
        voice = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(voice, language="en")
            print(text)
        except sr.UnknownValueError:
            print("UnknownValueError: Google Speech Recognition could not understand the audio.")
            return
        except sr.RequestError as e:
            print(f"RequestError: {e}")
            return
    translator = Translator(to_lang="hi")
    translation = translator.translate(text)
    print(translation)
    converted_audio = gTTS(translation, lang="hi")
    converted_audio.save(r"C:\Users\singh\OneDrive\Desktop\school\hello.mp3")

    # Play the audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\singh\OneDrive\Desktop\school\hello.mp3")
    pygame.mixer.music.play()

if __name__ == '__main__':
    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement == 0:
            continue
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Your personal assistant Sri is shutting down, Good bye')
            print('Your personal assistant Sri is shutting down, Good bye')
            break
        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open now")
            time.sleep(5)
        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(5)
        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail is open now")
            time.sleep(5)
        elif "weather" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"Temperature in kelvin units is {current_temperature}, "
                      f"humidity in percentage is {current_humidity}, "
                      f"description: {weather_description}")
                print(f"Temperature in kelvin = {current_temperature}\n"
                      f"Humidity (in percentage) = {current_humidity}\n"
                      f"Description = {weather_description}")
            else:
                speak("City Not Found")
        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(f"The time is {strTime}")
        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Sri version 1.0, your personal assistant. '
                  'I am programmed to do tasks like opening YouTube, Google, Gmail, predicting time, '
                  'searching Wikipedia, predicting weather, and answering computational or geographical questions!')
        elif "who made you" in statement or "who created you" in statement:
            speak("I was built by Shrishti, Ruchi and Shikha")
            print("I was built by Shrishti, Ruchi and Shikha")
        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is StackOverflow")
        elif 'news' in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, Happy reading')
            time.sleep(6)
        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")
        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)
        elif 'ask' in statement:
            speak('I can answer computational and geographical questions. What do you want to ask?')
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
            subprocess.call(["shutdown", "/l"])
        elif 'translate speech' in statement:
            translate_speech()
