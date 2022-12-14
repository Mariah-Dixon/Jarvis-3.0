import requests
from Functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from Functions.os_ops import open_calculator, open_photobooth, open_terminal, open_notes, open_discord, open_music
from random import choice
from utils import opening_text
from pprint import pprint
import webbrowser
import wolframalpha as wfa
import time
#import random
import json
import pickle
import numpy as np
import nltk
#from nltk.stem import WordNetLemmatizer
#import tensorflow as tf
#from tensorflow.keras.models import load_model
#My online_ops.py wasn't working. It could not access none of my api that I put in my env folder
#had to install dotenv. It will look for the .env file and it will load the environment variables from the file
#it will make the variables accesible to my project
from dotenv import load_dotenv
load_dotenv('/Users/mariahdixon/Code/Jarvis-3.0/Jarvis/.env')

# initialize elements
#lematizer = WordNetLemmatizer()
#intents = json.loads(open("intents.json").read())
#words = pickle.load(open("words.skl", "rb"))
#classes = pickle.load(open("classes.skl", "rb"))
#model = load_model("chatbotmodel.h5")

#cleaning up sentence function
#def clean_up_sentence(sentence):
#    sentence_words = nltk.word_tokenize(sentence)
#    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
#    return sentence_words

#sentence convert to bag of words (in binary 0 or 1)
#def bag_of_words(sentence):
#    sentence_words = clean_up_sentence(sentence)
#    bag = [0] * len(words)
#    for w in sentence_words:
#        for i, word in enumerate(words):
#            if word == w:
#                bag[i] = 1
#    return np.array(bag)

#predict function
#def predict_class(sentence):
#   bow = bag_of_words(sentence)
#   res = model.predict(np.array([bow]))[0]
#   ERROR_THRESHOLD = 0.25
#    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
#    results.sort(key=lambda x: x[1], reverse=True)
#    return_list = []
#    for r in results:
#        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
#    return return_list



USERNAME = config('USER')
BOTNAME = config('BOTNAME')

#Speech engine initialisation

engine = pyttsx3.init()

# Set Rate
engine.setProperty('rate', 170)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female or Male)
#def getvoices(voice):
voices = engine.getProperty('voices')
    #print(voices[0].id)
#    if voice == 1:
engine.setProperty('voice', voices[0].id)

#    if voice == 2:
#        engine.setProperty('voice', voices[1].id)

#    speak("hello this is jarvis")

#while True:
#    voice = int(input("Press 1 for male voice\nPress 2 for female voice\n"))
#    speak(audio)
#    getvoices(voice)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()

activationWord = 'Jarvis' #single word

# Greet the user
def greetMe():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    # now().hour function abstract’s the hour from the current time.
    if (hour >= 6) and (hour < 12):
    # If the hour is greater than zero and less than 12, the voice assistant wishes you with the message “Good Morning”
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
    # If the hour is greater than 12 and less than 16, the voice assistant wishes you with the following message “Good Afternoon”
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
     # If the hour is greater than 16 and less than 19, the voice assistant wishes you with the following message “Good Evening”
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

#Date function
def date():
    year = int(datetime.now().year)
    month = int(datetime.now().month)
    date = int(datetime.now().day)
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)

#Wolframalpha id
wolframa_id= "GVUJ8Q-P447KE2AG9"


#time function
def time():
    Time = datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(Time)

#Configure browser
#Set the path
chrome_path = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night ma'am, take care!")
            else:
                speak("Have a good day ma'am!")
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query

# Main Loop 
if __name__ == '__main__':
    greetMe()
    while True:
        query = take_user_input().lower() #My commands by me will be stored in the query and be converted to lower case

        #Open Notes on Laptop
        if 'open notes' in query:
            open_notes()

        #Open Discord app on laptop
        elif 'open discord' in query:
            open_discord()

        #Open Apple Music
        elif 'open music' in query:
            open_music()

        #Open Terminal 
        elif 'open command prompt' in query or 'open terminal' in query:
            open_terminal()

        #Open the photo booth app on laptop 
        elif 'open photo booth' in query:
            open_photobooth()

        #Open calculator app on laptop
        elif 'open calculator' in query:
            open_calculator()

        #Fetch my ip address
        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f"Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen ma'am.")
            print(f'Your IP Address is {ip_address}')

        #Search Wikipedia
        elif 'wikipedia' in query:
            speak("What do you want to search on Wikipedia, ma'am?")
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen ma'am.")
            print(results)

        #Play YouTube videos
        elif 'youtube' in query:
            speak("What do you want to play on Youtube, ma'am?")
            video = take_user_input().lower()
            play_on_youtube(video)

        #Search on google
        elif 'search on google' in query:
            speak("What do you want to search on Google, ma'am?")
            query = take_user_input().lower()
            search_on_google(query)

        #Send a Whatsapp message
        elif "send whatsapp message" in query:
            speak(
                "On what number should I send the message ma'am? Please enter in the console: ")
            number = input("Enter the number: ")
            speak("What is the message ma'am?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message ma'am.")

        #Send an Email
        elif "send an email" in query:
            speak("On what email address do I send mam? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject ma'am?")
            subject = take_user_input().capitalize()
            speak("What is the message ma'am?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email ma'am.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs ma'am.")

        #Tell me a joke 
        elif 'joke' in query:
            speak(f"Hope you like this one ma'am")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen ma'am.")
            pprint(joke)

        #Advice
        elif "advice" in query:
            speak(f"Here's an advice for you, ma'am")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen ma'am.")
            pprint(advice)

        #What are the new trending movies 
        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen ma'am.")
            print(*get_trending_movies(), sep='\n')

        #Tell me the news
        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines, ma'am")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen ma'am.")
            print(*get_latest_news(), sep='\n')

        #What is the Weather 
        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen ma'am.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        #Note Taking
        elif query[0] == 'log':
                speak("Ready to record your note, ma'am.")
                newNote = take_user_input().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(now)
                    newFile.write(' ')
                    newFile.write(newNote)
                speak('Note written')

        #Navigation
        elif query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                 # Assume the structure is activation word + go to, so let's remove the next two words
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

        #Remember a Note
        elif "remember that" in query:
            speak("What should I remember ma'am?")
            memory=take_user_input().lower()
            speak("You asked me to remember"+memory)
            remember=open("memory.txt","w")
            remember.write(memory)
            remember.close()

        elif "do you remember" in query:
            file=open("memory.txt","r")
            speak("You asked me to remember that "+file.read())


        #elif "calculate" in query:
			#app_id = "GVUJ8Q-P447KE2AG9"
			#client = wolframalpha.Client('GVUJ8Q-P447KE2AG9')
			#indx = query.lower().split().index('calculate')
			#query = query.split()[indx + 1:]
			#res = client.query(' '.join(query))
			#answer = next(res.results).text
			#print("The answer is " + answer)
			#speak("The answer is " + answer)


        elif "calculate" in query:
            client=wfa.Client(wolframa_id)
            index=query.lower().split().index("calculate")
            query=query.split()[index+1:]
            res=client.query("".join(query))
            answer=next(res.results).text
            print("The answer is: "+answer)
            speak("The answer is:"+answer)

        #time
        elif ('time' in query):
            time()

        #date
        elif 'date' in query:
            date()


        elif "who i am" in query: 
            speak("If you talk then definately you are human.") 
  
        elif "why you came to world" in query: 
            speak("Thanks to Mariah. further It's a secret") 

        elif "who made you" in query or "who created you" in query:  
            speak("I have been created by Mariah.")

        elif ("tell me your powers" in query or "help" in query
              or "features" in query):
            features = ''' i can help to do lot many things like..
            i can tell you the current time and date,
            i can tell you the current weather,
            i can tell you the News,
            i can create a reminder list,
            i can take Notes,
            i can send email to your boss or family or your friend,
            i can give you Advice,
            i can tell you non funny jokes,
            i can open any website,
            i can search things on wikipedia,
            I can search on google,
            And yes one more thing, Mariah is working on this system to add more features...,
            tell me what can i do for you??
            '''
            print(features)
            speak(features)
