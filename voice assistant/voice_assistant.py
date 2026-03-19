import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os

# ─── TTS ───
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print(f"\n🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ─── LISTEN ───
recognizer = sr.Recognizer()
recognizer.energy_threshold = 100
recognizer.dynamic_energy_threshold = True

def listen_command():
    with sr.Microphone() as source:
        print("\n🎤 Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            text = recognizer.recognize_google(audio, language="en-IN")
            print(f"👤 You said: \"{text}\"")
            return text.lower()
        except sr.WaitTimeoutError:
            print("⏱️  No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("❓ Could not understand.")
            return ""
        except sr.RequestError:
            speak("Internet connection needed for speech recognition")
            return ""

# ─── COMMANDS ───
def handle_command(command):
    if not command:
        return True

    with open("command_log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] {command}\n")

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open github" in command:
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")
    elif "open calculator" in command:
        os.system("calc")
        speak("Opening calculator")
    elif "open notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")
    elif "weather" in command:
        speak("Opening weather")
        webbrowser.open("https://www.weather.com")
    elif "battery" in command:
        import psutil
        b = psutil.sensors_battery()
        status = "charging" if b.power_plugged else "not charging"
        speak(f"Battery is at {int(b.percent)} percent and {status}")
    elif "joke" in command:
        import pyjokes
        speak(pyjokes.get_joke())
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    elif "wikipedia" in command or "wiki" in command:
        query = command.replace("wikipedia", "").replace("wiki", "").strip()
        speak(f"Opening Wikipedia for {query}")
        webbrowser.open(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
    elif "help" in command:
        speak("You can say: open google, open youtube, time, date, battery, joke, search for something, or stop.")
    elif "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye!")
        return False
    else:
        speak("Sorry, I did not understand that.")

    return True

# ─── MAIN ───
def run():
    hour = datetime.datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    speak(f"{greeting}! I am your voice assistant.")
    speak("Say help to hear available commands.")

    running = True
    while running:
        command = listen_command()
        running = handle_command(command)

if __name__ == "__main__":
    run()
