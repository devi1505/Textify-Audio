# Textify Audio

**Textify Audio** is a Python Flask app that converts call recordings (or any audio files) into text using OpenAI's Whisper model and stores the transcription in a MySQL database.

## Features
- Upload audio files (.mp3, .wav, .m4a, etc.)
- Convert speech to text using Whisper
- Store transcription in MySQL
- Display transcription on a web page

## Tech Stack
- Python 3.8+
- Flask
- Whisper (OpenAI)
- MySQL
- HTML (for upload page)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/devi1505/Textify-Audio.git
pip install flask
pip install openai-whisper
pip install torch
pip install mysql-connector-python
CREATE DATABASE call_text_db;

USE call_text_db;

CREATE TABLE transcriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(255),
    text LONGTEXT,
    language VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
python app.py
http://127.0.0.1:5000

---

This is **ready-to-use** — just create `README.md` in your project folder, paste this content, save it, and it will appear nicely on GitHub.  

Do you want me to now give the **final 5 simple commands to upload everything to GitHub**?
