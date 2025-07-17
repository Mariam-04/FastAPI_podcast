# FastAPI Podcast Generator

This is a FastAPI-based web service that generates a short podcast using a Large Language Model (LLM) and Eleven Labs Text-to-Speech API. You provide a topic, and it returns a scripted conversation (Host/Guest) along with the generated audio.

---

## Features

- Generates a podcast script using OpenAI (or other LLMs)
- Parses dialogue into segments for Host and Guest
- Converts each segment into audio using Eleven Labs API
- Combines the audio into a final `.mp3` podcast
- Exposes a FastAPI POST endpoint to generate podcasts via HTTP

---

## Project Structure

podcast_generator/

├── .env # API keys for OpenAI and Eleven Labs

├── requirements.txt # Project dependencies

├── podcast_generator.py # Core podcast generation logic (refactored)

├── main_api.py # FastAPI app with the /generate_podcast endpoint

└── README.md # Project documentation


---

## Setup Instructions

### 1. Clone the Repo

git clone https://github.com/Mariam-04/FastAPI_podcast.git
cd FastAPI_podcast

### 2. Create & Activate a Virtual Environment

python -m venv venv
venv\Scripts\activate     # On Windows
OR
source venv/bin/activate  # On macOS/Linux

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Add API Keys
Create a .env file with the following:

OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
