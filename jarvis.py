import os
import sys
import time
import datetime
import pyttsx3
import wikipedia
import webbrowser
import pyautogui
import urllib.parse
pyautogui.FAILSAFE = True

# Selenium & YouTube
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# Speech Recognition Setup
# =========================
try:
    import speech_recognition as sr
    mic_enabled = True
except Exception:
    print("[Warning] Speech recognition not available. Switching to text mode.")
    mic_enabled = False

# =========================
# Text-to-Speech Setup
# =========================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# =========================
# Greeting
# =========================
def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning, Sir. "
    elif hour < 18:
        greeting = "Good Afternoon, Sir. "
    else:
        greeting = "Good Evening, Sir. "
    greeting += "I am Jarvis. How can I help you today?"
    speak(greeting)
    time.sleep(0.5)

# =========================
# Take Command
# =========================
def takeCommand():
    if not mic_enabled:
        return input("Type your command: ")

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("Recognized:", query)
        return query
    except Exception:
        speak("Please repeat that.")
        return None

# =========================
# Selenium YouTube Player
# =========================
def play_youtube_song(song_name):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")

        driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
        driver.get(f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}")
        time.sleep(3)

        first_video = driver.find_element(By.ID, "video-title")
        first_video.click()
        time.sleep(3)

        # Click play if necessary
        try:
            play_button = driver.find_element(By.CLASS_NAME, "ytp-large-play-button")
            play_button.click()
        except:
            pass

        return driver
    except Exception as e:
        print("YouTube play error:", e)
        return None

# =========================
# NetMirror Player
# =========================
def play_netmirror(title_name):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")

        driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)

        # Open NetMirror
        driver.get("https://netmirror.app/")
        time.sleep(5)

        # Search box
        search_box = driver.find_element(By.TAG_NAME, "input")
        search_box.send_keys(title_name)
        time.sleep(2)
        search_box.send_keys(u'\ue007')  # ENTER key

        time.sleep(5)

        # Click first result
        first_result = driver.find_element(By.XPATH, "(//a)[1]")
        first_result.click()

        speak(f"Now playing {title_name} on NetMirror, Sir.")
        return driver

    except Exception as e:
        print("NetMirror error:", e)
        speak("Sorry Sir, NetMirror playback failed.")
        return None
    
# ================Open WhatsApp Web===============
def whatsapp(action, target=None, data=None):
    global whatsapp_driver

    try:
        # ================= OPEN WHATSAPP =================
        if action == "open":
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--user-data-dir=C:/JarvisChromeProfile")

            whatsapp_driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            whatsapp_driver.get("https://web.whatsapp.com")
            speak("WhatsApp Web is live, Sir. Scan QR if required.")
            time.sleep(15)

        # ================= SWITCH CHAT =================
        elif action == "switch":
            search = whatsapp_driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
            search.click()
            search.clear()
            search.send_keys(target)
            time.sleep(2)
            search.send_keys(Keys.ENTER)
            speak(f"Now chatting with {target}")

        # ================= SEND MESSAGE =================
        elif action == "send":
            box = whatsapp_driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
            box.click()
            box.send_keys(data)
            box.send_keys(Keys.ENTER)
            speak("Message delivered")

        # ================= TYPE ONLY =================
        elif action == "type":
            box = whatsapp_driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
            box.click()
            box.send_keys(data)
            speak("Text drafted")

        # ================= DELETE LAST =================
        elif action == "delete":
            last = whatsapp_driver.find_elements(By.CSS_SELECTOR, "div.message-out")[-1]
            last.click()
            time.sleep(1)

            menu = whatsapp_driver.find_element(By.XPATH, "//span[@data-icon='down-context']")
            menu.click()
            time.sleep(1)

            delete = whatsapp_driver.find_element(By.XPATH, "//div[contains(text(),'Delete')]")
            delete.click()
            time.sleep(1)

            confirm = whatsapp_driver.find_element(By.XPATH, "//div[contains(text(),'Delete for everyone')]")
            confirm.click()
            speak("Last message nuked successfully")

        # ================= ATTACH FILE =================
        elif action == "attach":
            clip = whatsapp_driver.find_element(By.XPATH, "//span[@data-icon='clip']")
            clip.click()
            time.sleep(1)

            file_box = whatsapp_driver.find_element(By.XPATH, "//input[@type='file']")
            file_box.send_keys(data)
            time.sleep(2)

            send = whatsapp_driver.find_element(By.XPATH, "//span[@data-icon='send']")
            send.click()
            speak("File dispatched")

        # ================= VOICE CALL =================
        elif action == "voice_call":
            btn = whatsapp_driver.find_element(By.XPATH, "//span[@data-icon='audio-call']")
            btn.click()
            speak("Dialing voice call")

        # ================= VIDEO CALL =================
        elif action == "video_call":
            btn = whatsapp_driver.find_element(By.XPATH, "//span[@data-icon='video-call']")
            btn.click()
            speak("Launching video call")

        # ================= END CALL =================
        elif action == "end_call":
            end = whatsapp_driver.find_element(By.XPATH, "//span[@data-icon='call-end']")
            end.click()
            speak("Call terminated")

    except Exception as e:
        print(e)
        speak("Operation failed, Sir")


# =========================
# Main Logic
# =========================
if __name__ == "__main__":
    wishMe()
    current_video_driver = None
    whatsapp_driver = None

    while True:
        query = takeCommand()
        if not query:
            continue
        query_lower = query.lower()

        # -------- CAPABILITIES --------
        if (
            "what" in query_lower
            and (
                "can you" in query_lower
                or "capable" in query_lower
                or "abilities" in query_lower
                or "what you do" in query_lower
            )
        ):
            speak(
                "I am capable of searching the web, opening and searching Google and YouTube, "
                "opening GitHub and TryHackMe, playing music, telling you the time, "
                "opening ChatGPT, and managing browser tabs and windows."
            )

        # -------- SEARCH --------
        elif "search" in query_lower:
            speak("Searching, Sir.")
            search_query = query_lower.replace("search", "").replace("for", "").strip()
            try:
                if "youtube" in query_lower:
                    search_query = search_query.replace("on youtube", "").strip()
                    speak(f"Searching YouTube for {search_query}, Sir.")
                    if current_video_driver:
                        current_video_driver.quit()
                    current_video_driver = play_youtube_song(search_query)
                    if not current_video_driver:
                        speak("Sorry Sir, I could not play that video.")
                elif "github" in query_lower:
                    search_query = search_query.replace("on github", "").strip()
                    speak(f"Searching GitHub for {search_query}, Sir.")
                    webbrowser.open(f"https://github.com/search?q={search_query.replace(' ', '+')}")
                else:
                    search_query = search_query.replace("on google", "").strip()
                    speak(f"Searching Google for {search_query}, Sir.")
                    webbrowser.open(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            except Exception:
                speak("Sorry Sir, I could not perform the search.")

        # -------- WIKIPEDIA --------
        elif "wikipedia" in query_lower:
            speak("Searching Wikipedia")
            wiki_query = query_lower.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(wiki_query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except Exception:
                speak("I could not find that information, Sir.")

        # -------- OPEN WEB --------
        elif "open youtube" in query_lower:
            webbrowser.open("https://youtube.com")
        elif "open google" in query_lower:
            webbrowser.open("https://google.com")
        elif "open github" in query_lower:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")
        elif "open try hack me" in query_lower or "open tryhackme" in query_lower:
            speak("Opening TryHackMe")
            webbrowser.open("https://tryhackme.com")
        elif "open chat gpt" in query_lower or "chat gpt" in query_lower:
            speak("Opening ChatGPT, Sir.")
            webbrowser.open("https://chat.openai.com/")
        elif "open smash" in query_lower or "open smash karts" in query_lower:
            speak("Opening Smash Karts, Sir.")
            webbrowser.open("https://smashkarts.io")
        elif "open net mirror" in query_lower:
            speak("Opening NetMirror, Sir.")
            webbrowser.open("https://netmirror.app")
        elif "ask chat gpt" in query_lower:
            speak("What do you want to ask ChatGPT, Sir?")
            question = takeCommand()
            if question:
                speak("Opening ChatGPT for your question.")
                encoded_question = urllib.parse.quote_plus(question)
                webbrowser.open(f"https://chat.openai.com/?prompt={encoded_question}")
            else:
                speak("No question detected, Sir.")
                
        # -------- WHATSAPP WEB CONTROLS --------

        elif "open WhatsApp" in query:
            whatsapp("open")

        elif "switch to" in query:
            name = query.replace("switch to","").strip()
            whatsapp("switch", name)

        elif "send message" in query:
            msg = query.replace("send message","").strip()
            whatsapp("send", data=msg)

        elif "type" in query:
            text = query.replace("type","").strip()
            whatsapp("type", data=text)

        elif "delete last message" in query:
            whatsapp("delete")

        elif "voice call" in query:
            whatsapp("voice_call")

        elif "video call" in query:
            whatsapp("video_call")

        elif "end call" in query:
            whatsapp("end_call")

                
        # -------- CLOSE TABS/WINDOWS --------
        elif "close" in query_lower:
            try:
                if "tab" in query_lower or "recent tab" in query_lower:
                    speak("Closing the current tab, Sir.")
                    pyautogui.hotkey("ctrl", "w")

                elif any(site in query_lower for site in ["youtube", "github", "google"]):
                    site = next(site for site in ["youtube", "github", "google"] if site in query_lower)
                    speak(f"Closing the {site.capitalize()} tab, Sir.")
                    pyautogui.hotkey("ctrl", "w")

                elif "browser" in query_lower or "chrome" in query_lower:
                    speak("Closing the browser window, Sir.")
                    pyautogui.hotkey("alt", "f4")

                else:
                    speak("Please specify what you want me to close, Sir.")

            except pyautogui.FailSafeException:
                speak(
                    "Fail safe triggered, Sir. "
                    "Please move the mouse away from the screen corners and try again."
                )

        # -------- play (YouTube) --------
        elif "play" in query_lower and "youtube" in query_lower:
            try:
                song_query = query_lower.replace("play", "").replace("on youtube", "").strip()
                if not song_query:
                    song_query = "trending music 2026"
                    speak("No song specified. Playing trending music, Sir.")
                else:
                    speak(f"Playing {song_query} on YouTube, Sir.")

                if current_video_driver:
                    current_video_driver.quit()
                current_video_driver = play_youtube_song(song_query)
                if not current_video_driver:
                    speak("Sorry Sir, I could not play that song.")
                else:
                    speak("Playing now. Enjoy, Sir.")

            except Exception:
                speak("An error occurred trying to play music, Sir.")

        # -------- play (NetMirror) --------
        elif "play" in query_lower and "netmirror" in query_lower:
            try:
                title_query = query_lower.replace("play", "").replace("on netmirror", "").strip()
                if not title_query:
                    speak("Please specify a title to play on NetMirror, Sir.")
                else:   
                    if current_video_driver:
                        current_video_driver.quit()
                    current_video_driver = play_netmirror(title_query)
            except Exception:
                speak("An error occurred trying to play on NetMirror, Sir.")
        
        # -------- TIME --------
        elif "time" in query_lower:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        # -------- EXIT --------
        elif "exit" in query_lower or "quit" in query_lower or "goodbye" in query_lower:
            try:
                speak("Goodbye, Sir. Shutting down.")
                engine.stop()
                if current_video_driver:
                    current_video_driver.quit()
            except:
                pass
            sys.exit()

        else:
            speak("I did not understand that command.")  