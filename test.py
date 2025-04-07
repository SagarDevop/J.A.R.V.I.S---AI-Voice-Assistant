if __name__ == "__main__":
    speak("Initializing jarvis....")
    is_listening = True  # Assistant starts in listening mode

if __name__ == "__main__":
    is_listening = False  # Start in sleep mode

    while True:
        try:
            with sr.Microphone() as source:
                if not is_listening:
                    print("Waiting for wake word (Jarvis)...")
                else:
                    print("Listening for command...")

                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

            text = r.recognize_google(audio).lower()
            print("Heard:", text)

            if text == "jarvis":
                speak("Welcome back, sir.")
                is_listening = True  # Activate listening mode

            elif is_listening:
                if not processCommand(text):  # If "stop" is said, stop listening
                    is_listening = False

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results, please check your internet connection.")
        except Exception as e:
            print(f"Error: {e}")
