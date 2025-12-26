import os
from flask import Flask, request, render_template
import whisper
import mysql.connector

# Tell Whisper where FFmpeg is
os.environ["PATH"] += os.pathsep + r"C:\Users\amarj\Desktop\ffmpeg-2025-12-24-git-abb1524138-essentials_build\bin"

app = Flask(__name__)

# Load Whisper model
model = whisper.load_model("base")

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="437561",   # <-- your MySQL password
    database="call_text_db"
)
cursor = db.cursor()

# -------------------------------
# HOME PAGE - Upload & Transcribe
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    transcription = ""

    if request.method == "POST":
        file = request.files["audio"]

        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        print("Processing:", filepath)

        result = model.transcribe(filepath)
        transcription = result["text"]

        # Save into MySQL
        sql = "INSERT INTO transcripts (filename, text) VALUES (%s, %s)"
        cursor.execute(sql, (file.filename, transcription))
        db.commit()

    return render_template("index.html", transcription=transcription)

# -------------------------------
# HISTORY PAGE
# -------------------------------
@app.route("/history")
def history():
    cursor.execute("SELECT filename, text, created_at FROM transcripts ORDER BY id DESC")
    records = cursor.fetchall()
    return render_template("history.html", records=records)

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
