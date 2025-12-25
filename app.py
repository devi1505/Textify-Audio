from flask import Flask, request, render_template_string
import whisper
import mysql.connector
import os

app = Flask(__name__)

# 🔹 MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="437561",  # Replace with your MySQL password
    database="call_text_db"
)
cursor = mydb.cursor()

# 🔹 Load Whisper model
model = whisper.load_model("small")

# 🔹 HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Textify Audio - MySQL Version</title>
<style>
body {font-family: Arial; text-align: center; margin-top: 50px;}
input {margin: 20px;}
</style>
</head>
<body>
<h1>🎤 Textify Audio (MySQL Version)</h1>
<p>Upload audio to convert to text</p>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="audio" required><br>
<button type="submit">Convert</button>
</form>
{% if text %}
<h2>Result:</h2>
<p>{{ text }}</p>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def upload_audio():
    text_output = ""
    
    if request.method == "POST":
        file = request.files["audio"]
        # Create uploads folder if not exist
        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # 🔹 Transcribe audio using Whisper
        result = model.transcribe(filepath)
        text_output = result["text"]

        # 🔹 Save to MySQL
        query = "INSERT INTO transcripts (filename, text) VALUES (%s, %s)"
        cursor.execute(query, (file.filename, text_output))
        mydb.commit()

    return render_template_string(HTML_PAGE, text=text_output)

if __name__ == "__main__":
    app.run(debug=True)
