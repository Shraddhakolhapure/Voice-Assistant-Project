import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import requests
import matplotlib.pyplot as plt  # Import Matplotlib for plotting
import calendar

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

API_KEY = 'b7d06ec7bcc681bcef0b8e6e781d0472'  # Replace with your API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# Define lists to store data
time_queries = []
query_lengths = []
query_words = []
user_intents = []

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def weather_info():
    city = 'Solapur'  # Replace with your city name
    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}"

    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data.get("cod") != "404":
        try:
            weather_description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']

            speak(f"The weather in {city} is {weather_description}. The temperature is {temperature} Kelvin.")
        except KeyError:
            speak("Weather information not available for this city.")
    else:
        speak("City not found.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"
    return query

def create_gui():
    root = tk.Tk()
    root.title("Voice Assistant")
    root.geometry("500x500")
    root.configure(bg='lightblue')

    label = tk.Label(root, text="Welcome to Voice Assistant", font=('Arial', 20), bg='lightblue')
    label.pack(pady=20)

    description_label = tk.Label(root, text="Voice Assistant Description:", font=('Arial', 12), bg='lightblue')
    description_label.pack()

    description_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    description_area.pack()

    description_text = (
        "This Voice Assistant can perform various tasks:\n"
        "- Open YouTube and Google\n"
        "- Play music\n"
        "- Provide the current time\n"
        "- Check Weather\n"
        "- Respond to general queries\n"
    )

    description_area.insert(tk.INSERT, description_text)
    description_area.configure(state='disabled')

    button_frame = tk.Frame(root, bg='lightblue')
    button_frame.pack(pady=20)

    start_button = tk.Button(button_frame, text="Start Assistant", command=start_assistant, font=('Arial', 14), bg='green', fg='white')
    start_button.grid(row=0, column=0, padx=10, pady=10)

    weather_button = tk.Button(button_frame, text="Check Weather", command=weather_info, font=('Arial', 14), bg='blue', fg='white')
    weather_button.grid(row=0, column=1, padx=10, pady=10)

    root.mainloop()

def start_assistant():
    speak("I'm ready to assist you.")

    while True:
        query = takeCommand().lower()

        # Collect data
        time_queries.append(datetime.datetime.now())
        query_lengths.append(len(query))
        query_words.extend(query.split())

        # Extract user intent
        if 'open youtube' in query:
            user_intent = 'Open YouTube'
        elif 'open google' in query:
            user_intent = 'Open Google'
        elif 'play music' in query:
            user_intent = 'Play Music'
        elif 'time' in query:
            user_intent = 'Get Time'
        elif 'exit' in query:
            user_intent = 'Exit'
        elif 'how are you' in query:
            user_intent = 'Ask How Are You'
        elif "who made you" in query:
            user_intent = 'Ask Who Made You'
        elif 'joke' in query:
            user_intent = 'Ask for Joke'
        elif 'your work' in query:
            user_intent = 'Ask About Your Work'
        elif 'when were you created' in query:
            user_intent = 'Ask When You Were Created'
        else:
            user_intent = 'Unknown'

        user_intents.append(user_intent)

        # Perform actions based on user query
        if 'open youtube' in query:
            speak("Here you go to Youtube")
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'play music' in query:
            music_file = r'C:\Users\kolha.SHRADDHA\Downloads\vandemataramflutebyrajeshcherthalaringtone-43151.mp3'
            os.startfile(music_file)
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'exit' in query:
            speak("Thanks for using the assistant.")
            break
        elif "how are you" in query:
            speak("I am fine, Thank you.")
        elif "who made you" in query:
            speak("I have been created by shraddha, namrata, and vidya.")
        elif 'joke' in query:
            speak("Here's a joke for you: Why don't scientists trust atoms? Because they make up everything!")
        elif 'your work' in query:
            speak("I'm here to assist you with various tasks such as providing information, playing music and more.")
        elif 'when were you created' in query:
            speak("I was created on October 25th, 2023.")
        else:
            speak("I don't have an answer for that. Please provide more specific commands.")

    # Perform data analysis and visualization
    analyze_time_queries()
    analyze_query_lengths()
    analyze_query_words()
    query_wordsby_hour()
    analyze_query_words_by_day()
    analyze_user_intents()
    analyze_user_intents_pie()
    analyze_query_length_vs_word_count()
    analyze_query_length_by_hour()

# Function to analyze time distribution of queries
def analyze_time_queries():
    plt.hist(time_queries, bins=24)  # Adjust bins as needed
    plt.xlabel('Hour of the Day')
    plt.ylabel('Frequency')
    plt.title('Time Distribution of Queries')
    plt.show()


def query_wordsby_hour():
    query_words_by_hour = [query_time.hour for query_time in time_queries]
    plt.hist(query_words_by_hour, bins=24)  # Adjust bins as needed
    plt.xlabel('Hour of the Day')
    plt.ylabel('Frequency')
    plt.title('Distribution of Query Words by Hour of the Day')
    plt.show()



def analyze_query_length_vs_word_count():
    query_length_word_count = [(len(query), len(query.split())) for query in query_texts]
    plt.scatter(*zip(*query_length_word_count))
    plt.xlabel('Query Length')
    plt.ylabel('Word Count')
    plt.title('Query Length vs. Word Count')
    plt.show()

def analyze_user_intents_pie():
    user_intents_count = {intent: user_intents.count(intent) for intent in set(user_intents)}
    labels, values = zip(*user_intents_count.items())
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Distribution of User Intents')
    plt.show()   

# Function to analyze distribution of query lengths
def analyze_query_lengths():
    plt.hist(query_lengths, bins=20)  # Adjust bins as needed
    plt.xlabel('Query Length')
    plt.ylabel('Frequency')
    plt.title('Distribution of Query Lengths')
    plt.show()

# Function to analyze distribution of query words
def analyze_query_words():
    plt.hist(query_words, bins=50)  # Adjust bins as needed
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.title('Distribution of Query Words')
    plt.show()




# Function to analyze distribution of query words by day of the week
def analyze_query_words_by_day():
    # Create a dictionary to store word frequencies for each day of the week
    day_word_counts = {day: {} for day in range(7)}  # 0: Monday, 1: Tuesday, ..., 6: Sunday

    # Iterate through time_queries and query_words to populate the dictionary
    for query_time, word in zip(time_queries, query_words):
        day_of_week = query_time.weekday()  # Get the day of the week (0: Monday, 1: Tuesday, ..., 6: Sunday)
        if word in day_word_counts[day_of_week]:
            day_word_counts[day_of_week][word] += 1
        else:
            day_word_counts[day_of_week][word] = 1

    # Plot the distribution of query words by day of the week
    for day, word_counts in day_word_counts.items():
        plt.bar(word_counts.keys(), word_counts.values())
        plt.xlabel('Word')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of Query Words for {calendar.day_name[day]}')
        plt.xticks(rotation=45)
        plt.show()


# Function to analyze distribution of user intents
def analyze_user_intents():
    user_intents_count = {intent: user_intents.count(intent) for intent in set(user_intents)}
    plt.bar(user_intents_count.keys(), user_intents_count.values())
    plt.xlabel('User Intent')
    plt.ylabel('Frequency')
    plt.title('Distribution of User Intents')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.show()

def analyze_query_length_by_hour():
    query_length_by_hour = [len(query) for query, hour in zip(query_texts, time_queries) if hour.hour != 0]
    plt.hist(query_length_by_hour, bins=24, align='left')
    plt.xlabel('Query Length')
    plt.ylabel('Frequency')
    plt.title('Distribution of Query Lengths by Hour of the Day')
    plt.xticks(range(0, 101, 10))
    plt.show()

if _name_ == '_main_':
    create_gui()
