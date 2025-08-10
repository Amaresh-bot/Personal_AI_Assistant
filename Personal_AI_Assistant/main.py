import os
import speech_recognition as sr
import win32com.client
import webbrowser
import openai
import datetime
from plyer import notification
import time
import pyautogui
import wikipedia
import webbrowser
import urllib.parse
import pywhatkit
import hugging_face_request
from hugging_face_request import generate_text


def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")  # changed to English
            print(f"User said: {query}")
            return query
        except Exception:
            print("Sorry, I couldn't understand.")
            return ""

def show_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5  # seconds
        )
    except Exception as e:
        print(f"Notification error: {e}")

def search_wikipedia(query):
    try:
        query = query.lower().replace("wikipedia", "").strip()
        results = wikipedia.summary(query, sentences=2)
        print("Wikipedia Summary:", results)  # This types (prints) the summary
        say("According to Wikipedia")
        say(results)
    except Exception as e:
        say("Sorry, I couldn't find any information on that.")
        print("Error:", e)

def search_google(query):
    # Remove the keyword "google" or "search" from query if present
    query = query.lower().replace("google", "").replace("search", "").strip()
    if query == "":
        say("Please tell me what to search on Google.")
        return
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    say(f"Searching Google for {query}")
    webbrowser.open(url)


def send_whatsapp_via_voice():
    say("Please tell me the phone number, without the country code.")
    phone_no = takeCommand().replace(" ", "")
    full_phone_no = "+91" + phone_no

    say("What message should I send?")
    message = takeCommand()

    if phone_no.isdigit() and len(phone_no) == 10:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 1

        if minute >= 60:
            minute = minute - 60
            hour = (hour + 1) % 24

        say(f"Sending your message to {full_phone_no} in 1 minute. Please keep the browser open.")
        pywhatkit.sendwhatmsg(full_phone_no, message, hour, minute)
    else:
        say("That phone number doesn't seem valid. Please try again.")

if __name__ == "__main__":
    say("Jarvis AI")
    while True:
        query = takeCommand()

        if not query:
            continue
        # --------- NEW TASK FEATURE ----------
        if "new task" in query.lower():
            task = query.lower().replace("new task", "").strip()
            if task != "":
                say(f"Adding task: {task}")  # Speak first
                time.sleep(0.5)  # Small pause to avoid overlap
                show_notification("New Task Added", task)  # Then show notification
            continue
        # -------------------------------------
        # --------- SHOW TASKS FEATURE ----------
        if "show all tasks" in query.lower() or "read tasks" in query.lower():
            if os.path.exists("todo.txt"):
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()
                    if tasks:
                        say("Here are your tasks:")
                        for t in tasks:
                            say(t.strip())
                    else:
                        say("You have no tasks.")
            else:
                say("No tasks found.")
            continue
            # ---------------------------------------
        # --------- CLEAR TASKS FEATURE ----------
        if "clear all tasks" in query.lower() or "delete tasks" in query.lower():
            if os.path.exists("todo.txt"):
                open("todo.txt", "w").close()
                say("All tasks have been cleared.")
            else:
                say("No tasks file found to clear.")
            continue
        # ----------------------------------------

        if "open" in query.lower():
            request = query.lower().replace("open", "").strip()
            pyautogui.press("win")  # Use 'win' for Windows key, not 'super'
            time.sleep(0.5)  # Small delay to let Start menu open
            pyautogui.write(request, interval=0.1)  # Type the app name slowly
            time.sleep(0.5)
            pyautogui.press("enter")

        if "search wikipedia" in query.lower():
            search_wikipedia(query)
            continue

        if "google" in query.lower() or "search" in query.lower():
            search_google(query)
            continue

        if "send whatsapp" in query.lower():
            send_whatsapp_via_voice()
            continue

        if "ask ai" in query.lower():
            say("What do you want to ask?")
            prompt = takeCommand()
            response = generate_text(prompt)
            print(response)
            say(response)
            continue

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["google", "https://www.google.com"],
            ["wikipedia", "https://www.wikipedia.org"],
            ["github", "https://www.github.com"],
            ["linkedin", "https://www.linkedin.com"],
            ["stack overflow", "https://stackoverflow.com"],
            ["twitter", "https://www.twitter.com"],
            ["instagram", "https://www.instagram.com"],
            ["facebook", "https://www.facebook.com"],
            ["netflix", "https://www.netflix.com"]
        ]

            ##SITIES
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]} sir..")
                webbrowser.open(site[1])

        songs = [
            ["chesededo", r"D:\Avinash\movies\Songs\01 - Chesededo.mp3"],
            ["daredumdadum", r"D:\Avinash\movies\Songs\02 - Daredumdadum.mp3"],
            ["chaala bagundi", r"D:\Avinash\movies\Songs\03 - Chaala Bagundi.mp3"],
            ["gopikamma", r"D:\Avinash\movies\Songs\04 - Gopikamma.mp3"],
            ["arere chandrakala", r"D:\Avinash\movies\Songs\05 - Arere Chandrakala.mp3"],
            ["nandalaala", r"D:\Avinash\movies\Songs\06 - Nandalaala.mp3"]
        ]
        # todo: here is your songs
        for song in songs:
            if f"play music {song[0]}" in query.lower():
                say(f"Playing {song[0]} sir..")
                os.startfile(song[1])

        apps = [
            ["powerpoint", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"],
            ["word", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"],
            ["github desktop",
             r"C:\Users\AVINASH\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\GitHub, Inc\GitHub Desktop.lnk"]
        ]

        for app in apps:
            if f"open {app[0]}" in query.lower():
                say(f"Opening {app[0]} sir..")
                os.startfile(app[1])

