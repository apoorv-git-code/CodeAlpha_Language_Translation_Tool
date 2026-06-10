🌐 Real-Time Language Translator
A lightweight, Python-powered translation tool featuring a clean user interface, instant language processing via an API, and automatic audio pronunciation generation.

✨ Features
Interactive User Interface: Simple layout allowing users to input text and pick source/target languages dynamically.

API-Driven Processing: Leverages a live translation engine API to compute natural translations instantly.

Automatic Language Selection: Supports multi-language translation pairings (English, Spanish, French, German, Italian, Japanese).

Audio Pronunciation (Bonus Feature): Converts the translated text into clear spoken audio using a built-in Text-to-Speech (TTS) engine.

🛠️ Tech Stack & Architecture
This project is built completely within the Python ecosystem, separating concerns cleanly between data fetching and user interaction.

Frontend Interface: Gradio — A modern UI framework for rapid machine learning and application prototyping.

Networking Client: requests — Sends data payloads securely to external translation services over HTTP.

Speech Synthesis Engine: gTTS (Google Text-to-Speech) — Generates local audio playbacks of foreign phrases.

How Data Flows
Plaintext
[ User Interface ]  ──(Text + Languages)──> [ Python Backend ]
                                                    │
                                            (HTTP GET Request)
                                                    │
                                                    ▼
[ User Screen ]  <──(Text + Audio File)─── [ Translation API ]
🚀 Getting Started
Prerequisites
Make sure you have Python 3.8 or higher installed on your machine.

1. Installation
Clone or download this repository, navigate to the folder in your terminal, and install the required library packages:

Bash
pip install gradio requests gtts
2. Running the Application
Launch the translation engine backend by running:

Bash
python app.py
3. Viewing the App
Once launched, the terminal will print out a local address:

Plaintext
Running on local URL:  http://127.0.0.1:7860
Open your web browser and navigate to [http://127.0.0.1:7860](http://127.0.0.1:7860) to access the live user interface.

📁 Code Overview
app.py: Contains the unified code engine.

LANGUAGE_MAP: Holds the ISO codes necessary for standardizing communication with the API.

translation_engine(): Handles the API requests, checks for HTTP error codes, and synthesizes audio files.

ui.Blocks(): Arranges widgets layouts (TextBoxes, Dropdowns, and Audio Players) into a user-friendly layout.
