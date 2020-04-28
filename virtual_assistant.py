import re
from time import ctime
from pygame import mixer
from gtts import gTTS
import speech_recognition as sr
import webbrowser
import requests
from bs4 import BeautifulSoup
import os


i = 0


def speak(audio_string):
    global i
    i = i + 1
    print(audio_string)
    tts = gTTS(text=audio_string, lang='en', slow=False)
    tts.save("audio" + str(i) + ".mp3")
    mixer.init()
    mixer.music.load("E:/Application/Python Project/Virtual Assistant/audio" + str(i) + ".mp3")
    #mixer.music.load("C:/Users/User/Downloads/05. Teri Ore.mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass


def my_command():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0, chunk_size=2048, sample_rate=48000) as source:
        print("Listening")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("you said ", command)
    except sr.UnknownValueError:
        print("Last command could not be heard")
        command = my_command()
    return command


def assistant(command):
    if 'search' in command:
        reg_ex = re.search('search (.+)', command)
        print(reg_ex.group(1))
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.google.com/maps/search/' + domain
            webbrowser.open(url)
            print('Done')
        else:
            pass

    elif 'find' in command:
        reg_ex = re.search('find (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.google.com/search?q='+domain
            webbrowser.open(url)
            print("Done")
        else:
            pass

    elif 'what is your name' in command:
        speak("Virtual Assistant")

    elif 'what are you doing' in command:
        speak('Doing my work')

    elif 'tell weather at' in command:
        reg_ex = re.search('tell weather at (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.wunderground.com/weather/in/' + domain
            webbrowser.open(url)
            print('Done')
        else:
            pass

    elif 'meaning' in command:
        reg_ex = re.search('meaning (.+)',command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://translate.google.com/#en/hi/'+domain
            webbrowser.open(url)
            print("Done")
        else:
            pass

    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/',
                           headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            speak(str(res.json()['joke']))
        else:
            speak('oops I ran out of Jokes')

    elif 'read' in command:
        reg_ex = re.search('read (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://en.wikipedia.org/wiki/'+domain
            data = requests.get(url).text
            soup = BeautifulSoup(data, "html.parser")
            tex = soup.find("div", {"class": "mw-body"}).p.text
            speak(tex)
            webbrowser.open(url)
            print("Done")

    elif 'play' in command:
        reg_ex = re.search('play (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = ''+domain
            webbrowser.open(url)
            print('Done')

    elif 'who are you' in command:
        speak('your personal assistant')

    elif 'reboot system' in command:
        os.system('reboot')

    elif 'time' in command:
        speak(ctime())

    elif 'help' in command:
        speak('Tell me your query.I can search for music/Information/Movie etc')

    else:
        speak("I don't know")


speak("I am ready to answer")

b = True
while b:
    assistant(my_command())
