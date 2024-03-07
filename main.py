from __future__ import with_statement
import pyttsx3
import openai
import subprocess
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import cv2
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from tempfile import gettempdir
from contextlib import closing



def speak(audio):
    polly = boto3.client('polly')

    try:
        response = polly.synthesize_speech(Text=audio, OutputFormat="mp3", VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)
    else:
        print("Could not stream audio")
        sys.exit(-1)

    if sys.platform == "win32":
        os.startfile(output)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
speak("Ready To Comply. What can I do for you ?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Could not find anything on wikipedia")
                print("Could not find anything on wikipedia")
        
        elif 'open youtube' in query:
            speak("what you will like to watch ?")
            qrry = takeCommand().lower()
            kit.playonyt(f"{qrry}")

        elif 'close chrome' in query:
            os.system("osascript -e 'tell application \"Google Chrome\" to quit'")

        elif 'play music' in query:
            music_dir = 'E:\Musics'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))

        elif 'stop music' in query:
            pyautogui.press('playpause')

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "open notes" in query:
            os.system("open /Applications/Notes.app")
        elif "close notes" in query: 
            os.system("killall Notes")


        elif "open command prompt" in query: 
            os.system("open -a Terminal .")
        elif "close command prompt" in query: 
            os.system("pkill Terminal")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("Error: Could not open the webcam.")
                speak("Error: Could not open the webcam.")
            else:
                while True:
                    ret, img = cap.read()
                    
                    if not ret:
                        print("Error: Unable to capture frame from the webcam.")
                        speak("Error: Unable to capture frame from the webcam.")
                        break

                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break

                cap.release()
                cv2.destroyAllWindows()

        elif "go to sleep" in query:
            speak(' alright then, I am switching off')
            sys.exit()

        elif "take screenshot" in query:
            speak('tell me a name for the file')
            name = takeCommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("screenshot saved")

        elif "calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("ready")
                print("Listning...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string=r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                '+' : operator.add,
                '-' : operator.sub,
                'x' : operator.mul,
                'divided' : operator.__truediv__,
                }[op]
            def eval_bianary_expr(op1,oper, op2):
                op1,op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)

            speak("your result is")
            speak(eval_bianary_expr(*(my_string.split())))

        elif "what is my ip address" in query:
            speak("Checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak("your ip adress is")
                speak(ipAdd)
            except Exception as e:
                speak("network is weak, please try again some time later")

        elif "volume up" in query:
            applescript = 'set volume output volume (output volume of (get volume settings) + 10)'
            subprocess.run(['osascript', '-e', applescript])
            time.sleep(1)
        elif "volume down" in query:
            applescript = 'set volume output volume (output volume of (get volume settings) - 10)'
            subprocess.run(['osascript', '-e', applescript])
            time.sleep(1)

        elif "mute" in query:
            applescript = 'set volume with output muted'
            subprocess.run(['osascript', '-e', applescript])
            time.sleep(1)



        elif "scroll down" in query:
            pyautogui.scroll(1000)

        elif "who are you" in query:
            print('I am your Virtual Assistant. I can control your desktop and search anything tou tell me too.')
            speak('I am your Virtual Assistant. I can control your desktop and search anything tou tell me too.')

        elif 'type' in query: #10
            query = query.replace("type", "") 
            pyautogui.write(f"{query}")


        elif 'open chrome' in query:
           os.system("open -a 'Google Chrome'")

        elif 'maximize this window' in query: 
            pyautogui.hotkey('alt', 'space') 
            time.sleep(1) 
            pyautogui.press('x')
        

        elif 'youtube search' in query:
            query = query.replace("youtube search", "") 
            pyautogui.hotkey('alt', 'd')
            time.sleep(1)
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.write(f"{query}", 0.1) 
            pyautogui.press('enter')

        elif 'open new window' in query: 
            pyautogui.hotkey('command', 't')

        elif 'open incognito window' in query: 
            pyautogui.hotkey('command', 'shift', 'n')
        
        elif 'maximize this window' in query: 
            pyautogui.hotkey('command', 'control', 'f')
            time.sleep(1) 

        elif 'minimise this window' in query: 
            pyautogui.hotkey('command', 'm') 
            time.sleep(1) 
        
        elif 'open history' in query:
            pyautogui.hotkey('command', 'y')
        elif 'open downloads' in query: 
            pyautogui.hotkey('option','command', 'l')
        elif 'previous tab' in query:
            pyautogui.hotkey('command', 'option', 'left')
        elif 'next tab' in query:
            pyautogui.hotkey('command', 'option', 'right')
        elif 'close tab' in query:
            pyautogui.hotkey('command', 'w')
        elif 'close window' in query:
            pyautogui.hotkey('command', 'w')

        elif 'clear browsing history' in query:
            pyautogui.hotkey('command', 'shift', 'backspace')
        
        elif 'search' in query:
            openai.api_key = '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'   #below code uses openai api to generate summary of the url

            
            prompt = query

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "What is the summary?"},
                ],
            )
            summary = response.choices[0].message.content
            print(summary)
            speak(summary)

