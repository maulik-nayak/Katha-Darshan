import pyttsx3
import time



def speak(text):

    engine = pyttsx3.init()
    print("Me:", text)

    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id) # 1 for female, 0 for male
    engine.setProperty('rate', 180) 
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.1)