import datetime
from dotenv import load_dotenv
import openai
import os
import pvcobra
import random
import struct
import sys
import textwrap
import threading
import time
import pvporcupine
import pyaudio
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from colorama import Fore
from openai import OpenAI
from pvleopard import *
from pvrecorder import PvRecorder
from threading import Thread
from time import sleep
from tavily import TavilyClient

# Variabile globale
audio_stream = None
cobra = None
pa = None
porcupine = None
recorder = None
wav_file = None
GPT_model = "gpt-3.5-turbo"

# Incarcare variabile environment
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pv_access_key = os.getenv("PV_ACCESS_KEY")
client = OpenAI(api_key=openai_api_key)
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Setare prompturile si log-ul de chat
prompt = ["How may I assist you?",
    "How may I help?",
    "What can I do for you?",
    "Ask me anything.",
    "Yes?",
    "I'm here.",
    "I'm listening.",
    "What would you like me to do?"]
chat_log=[
    {"role": "system", "content": "Your name is Glad-os. You do not have a namesake. You are a helpful AI-based assistant.Your answears are never longer than 50 words"},
    ]
should_tavily = ["look up", "search the web for", "the weather like", "up to date", "recent", "this year", "this month", "this week", "this day"]

# Functie de a sterge log-ul dupa 3 minute
def append_clear_countdown():
    sleep(180)
    global chat_log
    chat_log.clear()
    chat_log=[
        {"role": "system", "content": "Your name is Glad-os. You do not have a namesake. You are a helpful assistant."},
        ]    
    global count
    count = 0
    t_count.join

# Chat cu OpenAI API
def ChatGPT(query):
    user_query = [
        {"role": "user", "content": query},
        ]        
    send_query = (chat_log + user_query)
    response = client.chat.completions.create(
    model=GPT_model,
    messages=send_query
    )
    answer = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": answer})
    print(answer);
    return answer

# Web search cu Tavily
def TavilySearch(query):
    tavily = TavilyClient(api_key=tavily_api_key)
    all_context = tavily.search(query)
    user_query = [
        {"role": "user",
         "content": f'Information: """{all_context}"""\n\n' \
                    f'Using the above information, answer the following'\
                    f'query: "{query}" '},
        ]
    send_query = (chat_log + user_query)
    response = client.chat.completions.create(
    model=GPT_model,
    messages=send_query
    )
    answer = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": answer})
    print(answer);
    return answer

# Afisare timp curent
def current_time():
    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%m-%d-%Y %I:%M %p\n")
    print("The current date and time is:", formatted_time) 

# Detectare de liniste 
def detect_silence():
    cobra = pvcobra.create(access_key=pv_access_key)
    silence_pa = pyaudio.PyAudio()
    cobra_audio_stream = silence_pa.open(
                    rate=cobra.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=cobra.frame_length)
    last_voice_time = time.time()
    while True:
        cobra_pcm = cobra_audio_stream.read(cobra.frame_length)
        cobra_pcm = struct.unpack_from("h" * cobra.frame_length, cobra_pcm)
           
        if cobra.process(cobra_pcm) > 0.2:
            last_voice_time = time.time()
        else:
            silence_duration = time.time() - last_voice_time
            if silence_duration > 1.3:
                print("End of query detected\n")
                cobra_audio_stream.stop_stream                
                cobra_audio_stream.close()
                cobra.delete()
                last_voice_time=None
                break

# Ascultare cu Cobra pentru a detecta vocea
def listen():
    cobra = pvcobra.create(access_key=pv_access_key)
    listen_pa = pyaudio.PyAudio()
    listen_audio_stream = listen_pa.open(
                rate=cobra.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=cobra.frame_length)
    print("Asistentul te asculta...")
    while True:
        listen_pcm = listen_audio_stream.read(cobra.frame_length)
        listen_pcm = struct.unpack_from("h" * cobra.frame_length, listen_pcm)
        if cobra.process(listen_pcm) > 0.3:
            print("/voce detectata")
            listen_audio_stream.stop_stream
            listen_audio_stream.close()
            cobra.delete()
            break

def responseprinter(chat):
    wrapper = textwrap.TextWrapper(width=70)
    paragraphs = res.split('\n')
    wrapped_chat = "\n".join([wrapper.fill(p) for p in paragraphs])
    for word in wrapped_chat:
       #time.sleep(0.055)
       print(word, end="", flush=True)
    print()

# Functie de a reda vocea din text
def voice(chat):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=chat
    )
    with open("speech.mp3", "wb") as f:
        f.write(response.content)
    pygame.mixer.init()
    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    sleep(0.2)

# Detectarea cu Porcupine a cuvintelor de activare
def wake_word():
    porcupine = pvporcupine.create(keywords=["Glad-os"],
                            access_key=pv_access_key,
                            sensitivities=[0.5],
                                   )
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
   
    wake_pa = pyaudio.PyAudio()
    porcupine_audio_stream = wake_pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
   
    Detect = True
    while Detect:
        porcupine_pcm = porcupine_audio_stream.read(porcupine.frame_length)
        porcupine_pcm = struct.unpack_from("h" * porcupine.frame_length, porcupine_pcm)
        porcupine_keyword_index = porcupine.process(porcupine_pcm)
        if porcupine_keyword_index >= 0:
            print(Fore.GREEN + "\nWake word detected\n")
            current_time()
            porcupine_audio_stream.stop_stream
            porcupine_audio_stream.close()
            porcupine.delete()        
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
            Detect = False

# Inregistrare audio
class Recorder(Thread):
    keywords = ["search the web for", "look up"]
    def __init__(self):
        super().__init__()
        self._pcm = []
        self._is_recording = False
        self._stop = False
    def is_recording(self):
        return self._is_recording
    def run(self):
        self._is_recording = True
        recorder = PvRecorder(device_index=-1, frame_length=512)
        recorder.start()
        while not self._stop:
            self._pcm.extend(recorder.read())
        recorder.stop()
        self._is_recording = False
    def stop(self):
        self._stop = True
        while self._is_recording:
            pass
        return self._pcm

# Programul main
try:
    o = create(
        access_key=pv_access_key,
        )
   
    event = threading.Event()
    count = 0
    while True:
       
        try:
       
            Chat = 1
            if count == 0:
                t_count = threading.Thread(target=append_clear_countdown)
                t_count.start()
            else:
                pass  
            count += 1
            wake_word()
            voice(random.choice(prompt))
            recorder = Recorder()
            recorder.start()
            listen()
            detect_silence()
            transcript, words = o.process(recorder.stop())
            recorder.stop()
            print("You said: " + transcript)
            if Chat == 1:
                for item in should_tavily:
                    if item in transcript:
                        print("tavily was used\n\n")
                        (res) = TavilySearch(transcript)
                        break # If one is found, exit the loop
                else:
                    print("tavily was not used\n\n")
                    (res) = ChatGPT(transcript)
                print("\n GLaDOS a raspuns cu:\n")        
                t1 = threading.Thread(target=voice, args=(res,))
                t2 = threading.Thread(target=responseprinter, args=(res,))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            event.set()
            recorder.stop()
            o.delete
            recorder = None
           
        except openai.APIError as e:
            print("\nThere was an API error.  Please try again in a few minutes.")
            voice("\nThere was an A P I error.  Please try again in a few minutes.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            sleep(1)
        except openai.RateLimitError as e:
            print("\nYou have hit your assigned rate limit.")
            voice("\nYou have hit your assigned rate limit.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            break
        except openai.APIConnectionError as e:
            print("\nI am having trouble connecting to the API.  Please check your network connection and then try again.")
            voice("\nI am having trouble connecting to the A P I.  Please check your network connection and try again.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            sleep(1)
        except openai.AuthenticationError as e:
            print("\nYour OpenAI API key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program.")
            voice("\nYour Open A I A P I key or token is invalid, expired, or revoked.  Please fix this issue and then restart my program.")
            event.set()
            recorder.stop()
            o.delete
            recorder = None
            break
   
except KeyboardInterrupt:
    print("\nExiting GLaDOS Virtual Assistant")
    o.delete
