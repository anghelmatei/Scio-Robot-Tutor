# BucharestHackathon-GLaDOS

GLaDOS Virtual Assistant
Introduction
Welcome to the GLaDOS Virtual Assistant, a unique and engaging AI-powered assistant inspired by the iconic character from the Portal video game series. This Python script combines the power of OpenAI's language models, Porcupine's wake word detection, and Tavily's web search capabilities to create a snarky and witty virtual companion.

Features
Voice Interaction: The assistant can listen to your voice commands and respond with synthesized speech, creating a more natural and immersive user experience.
Snarky Personality: Channeling the spirit of GLaDOS, the assistant delivers responses with a touch of sarcasm and irony, adding a layer of humor to the interactions.
Integrated Web Search: The assistant can perform web searches using the Tavily API, providing up-to-date information on a variety of topics.
Persistent Chat Log: The chat log is maintained and cleared automatically after 3 minutes, ensuring a fresh and engaging conversation.
Error Handling: The script includes robust error handling, gracefully handling API errors, rate limits, and connection issues.
Requirements
To use the GLaDOS Virtual Assistant, you'll need the following:

Python 3.x
The following Python libraries:
datetime
dotenv
openai
os
pvcobra
random
struct
sys
textwrap
threading
time
pvporcupine
pyaudio
pygame
colorama
pvleopard
pvrecorder
tavily
API keys for OpenAI, Porcupine, and Tavily
Usage
Clone the repository and navigate to the project directory.
Create a .env file in the project directory and add your API keys:

Copy code
OPENAI_API_KEY=your_openai_api_key
PV_ACCESS_KEY=your_porcupine_access_key
TAVILY_API_KEY=your_tavily_api_key
Run the main.py script:

Copy code
python main.py
The assistant will start listening for the wake word "Glad-os". Once detected, it will prompt you to speak your request.
The assistant will then process your request, either using the Tavily web search or the OpenAI language model, and respond with synthesized speech.