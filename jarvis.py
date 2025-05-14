import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai
from langdetect import detect
import os
import json
from pathlib import Path
import time
from gtts import gTTS
import playsound






# Set up Gemini API
GEMINI_API_KEY = "AIzaSyDSsDGFKSe2gAJa1RbO01EsCxOrBGzW-CQ"
genai.configure(api_key=GEMINI_API_KEY)

# WeatherAPI.com (Free API Key required)
WEATHER_API_KEY = "271e6f0c33db4d5bac4102257250203"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

# Initialize speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# News API
NEWS_API_KEY = "efc697e2a9dc4fc6bc10679b0e271a6c"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Dictionary of music links
music = {
    "afsos": "https://youtu.be/2FhgKp_lfJQ?si=DM39iVkbdgzl7A5E",
    "bulleya": "https://youtu.be/_51KXfwcPMs?si=F-0i8K2K8_nqGJ-r",
    "zimedari": "https://youtu.be/eJCK2E6ocT0?si=O8SVvLtmW60iSMnC",
    "desi kalakar": "https://youtu.be/KhnVcAC5bIM?si=PNxEgG1yZzyi5q5u",
    "SAUDEBAZI" : "https://youtu.be/W4sHmzMCo8s?si=OSG66BWHU7E9d6zy",
    "Katto Gilehri" :  "https://youtu.be/KAkATnYbpbs?si=4k63_zGbLQ_kYAwe",
    "Laila Main Laila" : "https://youtu.be/jE4-tKSYScQ?si=HUhOHwJky3X1akBa",
    "Afghan Jalebi" : "https://youtu.be/zC3UbTf4qrM?si=HtVYWV7NRXnLo1EM",
    "Hookah Bar" : "https://youtu.be/b4b1cMVZOUU?si=-BygN8meQuSZn5C8",
    "Dupatta Tera" : "https://youtu.be/W2mjfazc9eM?si=zpCU_bA2ZCroCXUz",
    "Yeh Dil Deewana" : "https://youtu.be/_4Ft9UIKzwk?si=ZTBATfGq8m3wSap6",
    "Ghagra" : "https://youtu.be/caoGNx1LF2Q?si=acLe61gVcehaz5iW",
    "TERE MAST"  : "https://youtu.be/QWaXpiQwtpI?si=7VNi9qNwTpcu7pJp"


}

# Function to speak output
def speak(text):
    engine.say(text)
    engine.runAndWait()

def speakGemini(text, lang='hi'):  # Set default language to Hindi ('hi')
    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"temp_{time.time()}.mp3"
        temp_path = os.path.join(os.getcwd(), filename)
        tts.save(temp_path)
        playsound.playsound(temp_path)
        os.remove(temp_path)
    except Exception as e:
        print(f"TTS Error: {e}")

# Function to get weather updates
def get_weather(city):
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "yes"  # Disable air quality index to keep it simple
    }
    response = requests.get(WEATHER_API_URL, params=params)
    data = response.json()

    if "current" in data:
        weather = data["current"]
        temp = weather["temp_c"]
        condition = weather["condition"]["text"]
        return f"The weather in {city} is {condition} with a temperature of {temp}°C."
    else:
        return "Could not fetch weather data. Please check the city name."

# Function to fetch and speak news headlines
def get_news():
    params = {"apiKey": NEWS_API_KEY, "country": "us", "category": "general"}
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    if "articles" in data:
        headlines = [article["title"] for article in data["articles"][:5]]  # Get top 5 news headlines
        news_report = "Here are the latest news headlines: " + " ... ".join(headlines)
        return news_report
    else:
        return "Sorry, I couldn't fetch the news at the moment."
    
def load_cache():
    if os.path.exists("path.json"):
        with open("path.json", "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open("path.json", "w") as f:
        json.dump(cache, f, indent=4)



# def find_path_by_name(name, search_type="folder"):
#     ignore_dirs = [
#         "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", 
#         "C:\\ProgramData", "C:\\$Recycle.Bin", "C:\\System Volume Information"
#     ]

#     drives = [f"{d}:\\" for d in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]

#     for drive in drives:
#         for root, dirs, files in os.walk(drive):
#             # Normalize paths for comparison
#             normalized_root = os.path.normcase(root)
#             if any(normalized_root.startswith(os.path.normcase(bad_dir)) for bad_dir in ignore_dirs):
#                 continue  # Skip system folders

#             if search_type == "folder":
#                 for d in dirs:
#                     if name.lower() == d.lower():
#                         return os.path.join(root, d)
#             else:
#                 for f in files:
#                     if name.lower() == f.lower():
#                         return os.path.join(root, f)
#     return None



def find_exact_folder(folder_name):
    folder_name = folder_name.lower()
    search_roots = [
        Path.home() / "OneDrive" / "Desktop",  # Your Desktop
        Path("C:/")                            # Entire C drive
    ]

    for root in search_roots:
        for dirpath, dirnames, _ in os.walk(root):
            for dirname in dirnames:
                if dirname.lower() == folder_name:
                    return os.path.join(dirpath)  # Return exact folder match path
    return None




# Function to process user commands using Gemini API
def processCommand(command):
    command = command.lower()  # Convert to lowercase for consistency

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play "):  # Check if command starts with "play"
        song_name = command.split("play ", 1)[1].strip().lower()
        music_lower = {key.lower(): value for key, value in music.items()}  # Extract song name
        if song_name in music_lower:
            speak(f"Playing {song_name}")
            webbrowser.open(music_lower[song_name])
        else:
            speak("Sorry, this song is not in the library.")

    elif "what's the weather in" in command or "what is the weather in" in command  or "tell me weather condtion in" in command  or "current weather " in command:
        city = command.split("in")[-1].strip()
        weather_info = get_weather(city)
        speak(weather_info)

    elif "tell me the news" in command or "what's the news" in command:
        news_info = get_news()
        speak(news_info)

    elif "who developed you" in command or "who made you" in command:
        speak("I was developed by Divas singh and his team.")



    # Create file command
    elif "create file" in command:
        try:
            parts = command.replace("create file", "").strip().split(" in ")
            file_name = parts[0].strip()
            parent_name = parts[1].strip().lower() if len(parts) > 1 else ""

            if parent_name:
                if parent_name == "desktop":
                    # Use OneDrive Desktop path
                    parent_path = os.path.join(os.environ["OneDrive"], "Desktop")
                else:
                    parent_path = find_path_by_name(parent_name, search_type="folder")

                if parent_path:
                    file_path = os.path.join(parent_path, file_name)
                    with open(file_path, "w") as f:
                        f.write("")  # Create an empty file
                    speak(f"File '{file_name}' has been created in '{parent_name}'.")
                    print(f"Created at: {file_path}")
                else:
                    speak(f"Folder '{parent_name}' not found.")
            else:
                file_path = os.path.join(os.getcwd(), file_name)
                with open(file_path, "w") as f:
                    f.write("")
                speak(f"File '{file_name}' created in current directory.")
        except Exception as e:
            speak("An error occurred while creating the file.")
            print(e)


    # Create folder command
    elif "create folder" in command:
        try:
            parts = command.replace("create folder", "").strip().split(" in ")
            folder_name = parts[0].strip()
            parent_name = parts[1].strip().lower() if len(parts) > 1 else ""

            if parent_name:
                parent_path = find_exact_folder(parent_name)
                if parent_path:
                    folder_path = os.path.join(parent_path, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    speak(f"Folder '{folder_name}' has been created in '{parent_name}'.")
                    print(f"Created at: {folder_path}")
                else:
                    speak(f"Folder '{parent_name}' not found.")
            else:
                folder_path = os.path.join(os.getcwd(), folder_name)
                os.makedirs(folder_path, exist_ok=True)
                speak(f"Folder '{folder_name}' created in current directory.")
        except Exception as e:
            speak("An error occurred while creating the folder.")
            print(e)
  


    elif "open" in command:
        try:
            target = command.replace("open", "").replace("folder", "").replace("file", "").strip().lower()

            # Load cache
            cache = load_cache()

            # If already in cache, open it
            if target in cache:
                speak(f"Opening cached {target}")
                os.startfile(cache[target])
                return

            speak(f"Searching the whole system for {target}. This may take a while...")

            # Drives to search (you can add more)
            drives = [f"{d}:\\" for d in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]

            found = None
            for drive in drives:
                for root, dirs, files in os.walk(drive):
                    for name in dirs + files:
                        if target in name.lower():
                            found = os.path.join(root, name)
                            break
                    if found:
                        break
                if found:
                    break

            if found:
                speak(f"Found and opening {target}")
                os.startfile(found)
                cache[target] = found
                save_cache(cache)
            else:
                speak("Sorry, I couldn't find that file or folder.")

        except Exception as e:
            speak("An error occurred while trying to open the file or folder.")
            print(e)

        

    else:
        # Let Gemini generate a smart response
        speak("Thinking...")
        response = get_gemini_response(command)
        speakGemini(response)

# Function to get response from Gemini AI
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I'm having trouble processing your request right now."

# Main function
if __name__ == "__main__":
    speak("Initializing jarvis....")
    print("Waiting for wake word (Jarvis)...")
    is_listening = False  # Assistant starts in listening mode

while True:
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()
            print("Heard:", text)
            if text == "jarvis":
               speak("Welcome back, sir.")
               print("Listening for command...")
               is_listening = True  # Activate listening mode

            elif text == "stop":
               speak("bye sir, call me if you need")
               is_listening = False  # Deactivate listening mode

            elif is_listening:
                processCommand(text)
                if not is_listening:
                    print("Waiting for wake word (Jarvis)...")
            else:
                print("Listening for command...")

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results, please check your internet connection.")
    except Exception as e:
        print(f"Error: {e}")
        
