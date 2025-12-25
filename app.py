from flask import Flask, request, render_template
import os
import whisper
import mysql.connector

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model
model = whisper.load_model("base")

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",  # replace with your MySQL password
    database="call_text_db"
)
cursor = mydb.cursor()

def convert_audio_to_text(filepath, language=None):
    if language:
        result = model.transcribe(filepath, language=language)
    else:
        result = model.transcribe(filepath)
    return result["text"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    file = request.files["audiofile"]
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Convert audio to text
        text = convert_audio_to_text(filepath)

        # Save to DB
        sql = "INSERT INTO transcriptions (file_name, text) VALUES (%s, %s)"
        cursor.execute(sql, (file.filename, text))
        mydb.commit()

        return f"<h2>Transcription:</h2><p>{text}</p>"

    return "No file uploaded!"

if __name__ == "__main__":
    app.run(debug=True)
