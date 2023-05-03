import pyttsx3
import speech_recognition as sr
import webbrowser
import tkinter as tk
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

root = tk.Tk()
root.title('Mycroft Virtual Assistant')
root.geometry('400x400')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hour = int(time.strftime('%H'))
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Welcome, I am your personal assistant")

def VoiceCommand(text_area):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        text_area.insert(tk.END, "Listening...\n")
    try:
        query = r.recognize_google(audio, language='en-in')
        text_area.insert(tk.END, "You said: " + query + "\n")
        return query
    except Exception as e:
        text_area.insert(tk.END, "Sorry, I didn't understand that. Please try again.\n")
        return None

def search_google(query):
    search_url = "https://www.google.com/search?q=" + query
    webbrowser.open(search_url)

def on_click(text_area):
    command = VoiceCommand(text_area)
    if command is not None:
        speak("You said: " + command)

def done(text_area):
    query = text_area.get("1.0", tk.END).strip()
    if query:
        search_google(query)
    else:
        text_area.insert(tk.END, "Please say something to search.\n")

label = tk.Label(root, text='Press the button and speak')
label.pack(pady=10)

text_area = tk.Text(root, height=10, width=50)
text_area.pack(pady=10)

button = tk.Button(root, text='Speak', command=lambda: on_click(text_area))
button.pack(pady=10)

done_button = tk.Button(root, text='Done', command=lambda: done(text_area))
done_button.pack(pady=10)

greet()

while True:
    current_time = time.strftime('%H:%M:%S')
    label.config(text='Current Time: ' + current_time)
    root.update()
    time.sleep(1)
