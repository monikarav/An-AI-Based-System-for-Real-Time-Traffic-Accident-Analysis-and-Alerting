from flask import Flask, render_template, request, send_from_directory
import os
import cv2
import numpy as np
import time
import sqlite3
from datetime import datetime
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Model
model = load_model("accident_model.keras")

# --------------------------------------------------
# Database Setup
# --------------------------------------------------

def init_db():
    conn = sqlite3.connect("accident_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result TEXT,
            confidence REAL,
            location TEXT,
            processing_time REAL,
            date_time TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# --------------------------------------------------
# Helper
# --------------------------------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --------------------------------------------------
# Video Analysis
# --------------------------------------------------

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    start_time = time.time()

    accident_detected = False
    max_confidence = 0
    total_frames = 0
    accident_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        if total_frames % 5 != 0:
            continue

        img = cv2.resize(frame, (224, 224))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img, verbose=0)
        confidence = float(prediction[0][0])

        if confidence > max_confidence:
            max_confidence = confidence

        if confidence > 0.5:
            accident_detected = True
            accident_frames += 1

    cap.release()

    processing_time = round(time.time() - start_time, 2)

    if accident_detected:
        result_text = "Accident Detected 🚨"
        final_confidence = round(max_confidence * 100, 2)
    else:
        result_text = "No Accident Detected 🟢"
        final_confidence = round((1 - max_confidence) * 100, 2)

    return {
        "result": result_text,
        "confidence": final_confidence,
        "total_frames": total_frames,
        "accident_frames": accident_frames,
        "processing_time": processing_time
    }

# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/history")
def history():
    conn = sqlite3.connect("accident_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template("history.html", records=records)


@app.route("/analyze", methods=["POST"])
def analyze():

    if "video" not in request.files:
        return "No video file found"

    video = request.files["video"]
    location = request.form.get("location", "Unknown Location")

    if video.filename == "":
        return "No selected file"

    if video and allowed_file(video.filename):

        filename = secure_filename(video.filename)
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        video.save(video_path)

        data = analyze_video(video_path)

        # Save to database
        conn = sqlite3.connect("accident_history.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO history (result, confidence, location, processing_time, date_time)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["result"],
            data["confidence"],
            location,
            data["processing_time"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            result=data["result"],
            confidence=data["confidence"],
            video_file=filename,
            total_frames=data["total_frames"],
            accident_frames=data["accident_frames"],
            processing_time=data["processing_time"],
            location=location
        )

    return "Invalid file type."


# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
