import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import pygetwindow as gw
import os
import time
import threading
import pyautogui

# Initialize the recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that.")
            return "None"
        except sr.RequestError as e:
            speak("Sorry, my speech service is down.")
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"

# Function to search Google in the browser
def search_google(query):
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to search YouTube in the browser
def search_youtube(query):
    speak(f"Searching YouTube for {query}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

# Function to minimize a specific window
def minimize_window(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            windows[0].minimize()
            speak(f"Window '{window_title}' minimized.")
        else:
            speak(f"No window with title '{window_title}' found.")
    except Exception as e:
        speak("Sorry, I couldn't minimize the window.")
        print(e)

# Function to maximize a specific window
def maximize_window(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            windows[0].maximize()
            speak(f"Window '{window_title}' maximized.")
        else:
            speak(f"No window with title '{window_title}' found.")
    except Exception as e:
        speak("Sorry, I couldn't maximize the window.")
        print(e)

# Function to open an application
def open_application(app_name):
    try:
        if 'notepad' in app_name:
            os.system('start notepad')
            speak("Opening Notepad.")
            time.sleep(2)  # Wait a bit longer to ensure the window opens
            windows = [win for win in gw.getWindowsWithTitle('Notepad') if win.title.startswith('Untitled - Notepad')]
            if windows:
                windows[0].activate()
                speak("Notepad is open.")
                print("Debug: Notepad window found and activated.")
            else:
                speak("Sorry, I couldn't find the Notepad window.")
                print("Debug: Notepad window not found.")
        elif 'calculator' in app_name:
            os.system('start calc')
            speak("Opening Calculator.")
            time.sleep(2)
            windows = gw.getWindowsWithTitle('Calculator')
            if windows:
                windows[0].activate()
                speak("Calculator is open.")
                print("Debug: Calculator window found and activated.")
            else:
                speak("Sorry, I couldn't find the Calculator window.")
                print("Debug: Calculator window not found.")
        elif 'paint' in app_name:
            os.system('start mspaint')
            speak("Opening Paint.")
        # Add more applications as needed
        else:
            speak(f"Sorry, I can't open {app_name}.")
            print(f"Debug: {app_name} not supported.")
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}.")
        print(e)

# Function to open a folder
def open_folder(folder_path):
    try:
        os.startfile(folder_path)
        speak(f"Opening {folder_path}.")
        print(f"Debug: Opening folder {folder_path}.")
    except Exception as e:
        speak(f"Sorry, I couldn't open the folder {folder_path}.")
        print(e)

# Function to control volume
def control_volume(action):
    try:
        if action == 'volume up':
            pyautogui.press("volumeup")
            speak("Volume increased.")
        elif action == 'volume down':
            pyautogui.press("volumedown")
            speak("Volume decreased.")
        elif action == 'mute':
            pyautogui.press("volumemute")
            speak("Volume muted.")
    except Exception as e:
        speak(f"Sorry, I couldn't {action}.")
        print(e)

# Function to scroll up or down slowly until "stop scroll" is said
def scroll(direction):
    try:
        while True:
            if direction == 'up':
                pyautogui.scroll(10)
            elif direction == 'down':
                pyautogui.scroll(-10)
            time.sleep(0.1)
            command = listen()
            if 'stop scroll' in command:
                speak("Stopping scrolling.")
                break
    except Exception as e:
        speak("Sorry, I couldn't scroll.")
        print(e)

# Function to respond to commands
def respond(command):
    if 'hello' in command:
        speak("Hello! How can I assist you today?")
    elif 'time' in command:
        current_time = datetime.now().strftime('%H:%M')
        speak(f"The current time is {current_time}.")
    elif 'date' in command:
        current_date = datetime.now().strftime('%Y-%m-%d')
        speak(f"Today's date is {current_date}.")
    elif 'year' in command:
        current_year = datetime.now().strftime('%Y')
        speak(f"This year is {current_year}.")
    elif 'search' in command:
        query = command.replace('search', '').strip()
        if query:
            search_google(query)
        else:
            speak("What do you want to search for?")
    elif 'youtube' in command:
        query = command.replace('youtube', '').strip()
        if query:
            search_youtube(query)
        else:
            speak("What do you want to search for on YouTube?")
    elif 'minimize' and 'minimise' in command:
        speak("Which window would you like to minimize?")
        window_title = listen()
        if window_title and window_title != "none":
            minimize_window(window_title)
    elif 'maximize' in command:
        speak("Which window would you like to maximize?")
        window_title = listen()
        if window_title and window_title != "none":
            maximize_window(window_title)
    elif 'open' in command:
        if 'folder' in command:
            folder_path = command.replace('open folder', '').strip()
            if folder_path:
                open_folder(folder_path)
            else:
                speak("Which folder do you want to open?")
        elif 'this pc' in command:
            open_folder('This PC')
        else:
            app_name = command.replace('open', '').strip()
            if app_name:
                open_application(app_name)
            else:
                speak("What application do you want to open?")
    elif 'volume up' in command:
        control_volume('volume up')
    elif 'volume down' in command:
        control_volume('volume down')
    elif 'mute' in command:
        control_volume('mute')
    elif 'scroll up' in command:
        speak("Scrolling up.")
        scroll('up')
    elif 'scroll down' in command:
        speak("Scrolling down.")
        scroll('down')
    elif 'how made you' in command or 'who made you' in command:
        speak("Anurag created me.")
    elif 'stop' in command or 'exit' in command:
        return False
    else:
        speak("I'm not sure how to help with that.")
    return True

# GUI class for the voice assistant
class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("600x400")  # Increased window size
        self.root.configure(bg="#87CEEB")

        self.label = tk.Label(root, text="Voice Assistant", bg="#87CEEB", fg="#333333", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening, bg="#4caf50", fg="#ffffff", font=("Helvetica", 12))
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Stop Listening", command=self.stop_listening, bg="#ff5722", fg="#ffffff", font=("Helvetica", 12))
        self.stop_button.pack(pady=20)

        self.result_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.about_button = tk.Button(root, text="About", command=self.show_about, bg="#2196f3", fg="#ffffff", font=("Helvetica", 12))
        self.about_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#ff5722", fg="#ffffff", font=("Helvetica", 12))
        self.exit_button.pack(pady=10)

        self.listening = False
        speak("Yes sir! I am now ready.")

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.result_label.config(text="Listening...")
            self.start_button.config(bg="grey")  # Change to grey when clicked
            threading.Thread(target=self.listen_loop).start()

    def listen_loop(self):
        while self.listening:
            command = listen()
            if command and command != "none":
                self.result_label.config(text=f"You said: {command}")
                if not respond(command):
                    self.stop_listening()
            else:
                self.result_label.config(text="Listening...")  # Ensure "Listening..." text reappears

    def stop_listening(self):
        self.listening = False
        self.result_label.config(text="Listening stopped.")
        self.start_button.config(bg="#4caf50")  # Reset to original green color

    def show_about(self):
        about_text = (
            "This is a simple Voice Assistant to perform various tasks using voice commands.\n"
            "Functions:\n"
            "1. Respond to Greetings: The assistant can respond to greetings like 'hello'.\n"
            "2. Tell Time and Date: It can provide the current time and date, including the year.\n"
            "3. Web Search: The assistant can perform Google searches based on user queries.\n"
            "4. YouTube Search: The assistant can perform YouTube searches based on user queries.\n"
            "5. Open Applications: The assistant can open applications like Notepad, Calculator, and Paint.\n"
            "6. Open Folders: The assistant can open specific folders.\n"
            "7. Open 'This PC': The assistant can open 'This PC'.\n"
            "8. Minimize Window: The assistant can minimize the active window.\n"
            "9. Maximize Window: The assistant can maximize the active window.\n"
            "11.Scroll up and scroll down.\n"
            "12. Stop Listening: The listening loop can be stopped by saying 'stop' or 'exit'.\n\n\n\n"
            "Created By Anurag Kumar\nUsing Python Language."
        )
        messagebox.showinfo("About", about_text)

# Main function
def main():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
