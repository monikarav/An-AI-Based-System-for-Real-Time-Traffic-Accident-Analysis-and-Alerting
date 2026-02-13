# 🚦 AccidentGuard: Video-Based Accident Detection System

The AccidentGuard system is an intelligent video analytics platform designed to automatically detect road accidents from uploaded traffic or surveillance videos. By leveraging computer vision and machine learning techniques along with a user-friendly web interface, the system helps authorities and organizations identify accident events efficiently and respond in a timely manner.

---

## 📘 About

AccidentGuard applies computer vision and deep learning concepts to analyze video streams and identify accident occurrences. Traditional monitoring relies on manual surveillance, which leads to slow response times. This project addresses this by automating accident detection, allowing faster emergency response and smarter traffic management.

---

## ✨ Features

- Automated accident detection from uploaded video files  
- Frame-by-frame video analysis using computer vision  
- Machine learning–ready architecture (CNN extendable)  
- Web-based application for easy interaction  
- Visual result display with accident status  
- Secure execution without API keys or tokens  
- Scalable and modular system design  

---

## 🛠️ Requirements

### Operating System
- 64-bit Windows 10 / Ubuntu / Google Colab

### Development Environment
- Python 3.8 or later

### Libraries & Frameworks
- OpenCV  
- NumPy  
- Scikit-learn / CNN models (optional)  
- Streamlit  

### Tools & IDE
- VS Code / Google Colab  
- Git / Git LFS  

---

## 🧱 System Architecture

The system follows a modular architecture: users upload traffic videos → backend extracts frames and applies detection logic → results displayed on the web interface. This ensures scalability, modularity, and separation of concerns.

---

## Accident_detection_system.py

```python
import cv2
import numpy as np

def detect_accident(video_path):
    cap = cv2.VideoCapture(video_path)
    accident_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Example detection logic
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Simple threshold: if too many edges, flag accident
        if np.sum(edges) > 1e6:
            accident_detected = True
            break

    cap.release()
    return accident_detected

video_file = 'uploads/test_video.mp4'
result = detect_accident(video_file)
if result:
    print("🚨 Accident Detected")
else:
    print("✅ No Accident")
```
## Home.html
```
<!DOCTYPE html>
<html>
<head>
    <title>AI Accident Detection</title>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

    <style>
        * { 
            margin:0; 
            padding:0; 
            box-sizing:border-box; 
            font-family:'Poppins',sans-serif; 
        }

        body {
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#000000);
            background-size:400% 400%;
            animation:gradientBG 12s ease infinite;
        }

        @keyframes gradientBG {
            0%{background-position:0% 50%;}
            50%{background-position:100% 50%;}
            100%{background-position:0% 50%;}
        }

        .card {
            width:450px;
            padding:40px;
            border-radius:20px;
            background:rgba(255,255,255,0.08);
            backdrop-filter:blur(20px);
            text-align:center;
            color:white;
            box-shadow:0 20px 40px rgba(0,0,0,0.5);
        }

        h1 { 
            margin-bottom:25px; 
        }

        .upload-box {
            border:2px dashed #38bdf8;
            padding:20px;
            border-radius:15px;
            margin-bottom:20px;
            cursor:pointer;
            transition:0.3s;
        }

        .upload-box:hover { 
            background:rgba(255,255,255,0.1); 
        }

        input[type="file"] { 
            display:none; 
        }

        input[type="text"] {
            width:100%;
            padding:12px;
            border-radius:10px;
            border:none;
            margin-bottom:15px;
        }

        button {
            padding:12px 25px;
            border-radius:30px;
            border:none;
            font-size:16px;
            background:linear-gradient(90deg,#00c6ff,#0072ff);
            color:white;
            cursor:pointer;
            transition:0.3s;
        }

        button:hover { 
            transform:scale(1.05); 
        }

        .loader { 
            margin-top:15px; 
            display:none; 
        }

        .gps-status{
            font-size:12px;
            margin-bottom:10px;
            opacity:0.8;
        }

        .history-link{
            margin-top:20px;
            display:block;
            color:#38bdf8;
            text-decoration:none;
        }

    </style>
</head>

<body>

<div class="card">
    <h1>🚗 AI Accident Detection</h1>

    <form action="/analyze" method="POST" enctype="multipart/form-data" onsubmit="showLoader()">

        <!-- Upload -->
        <label class="upload-box">
            📁 Click to Upload Video
            <input type="file" name="video" required>
        </label>

        <!-- Manual Location Input -->
        <input type="text" id="manualLocation" placeholder="Enter Location (Optional)">

        <!-- Hidden GPS Field -->
        <input type="hidden" name="location" id="locationInput">

        <div class="gps-status" id="gpsStatus">
            📍 Detecting GPS location...
        </div>

        <button type="submit">Analyze Now</button>

        <div class="loader" id="loader">
            ⏳ AI is analyzing your video...
        </div>

    </form>

    <a href="/history" class="history-link">📊 View Accident History</a>

</div>

<script>

// Show Loader
function showLoader(){
    document.getElementById("loader").style.display="block";

    // If manual location filled → use it
    const manual = document.getElementById("manualLocation").value;
    if(manual.trim() !== ""){
        document.getElementById("locationInput").value = manual;
    }
}

// Auto GPS Detection
navigator.geolocation.getCurrentPosition(
    function(position){
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById("locationInput").value =
            "Lat: " + latitude + ", Lon: " + longitude;

        document.getElementById("gpsStatus").innerText =
            "📍 GPS Location Auto-Detected";
    },
    function(){
        document.getElementById("gpsStatus").innerText =
            "⚠ GPS Permission Denied (Enter manually)";
    }
);

</script>

</body>
</html>
```
## Result.html

```
<!DOCTYPE html>
<html>
<head>
<title>AI Accident Analysis</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Poppins',sans-serif;
}

body{
    background:#050816;
    color:white;
    padding:40px;
}

/* Neon Text */
.neon-text{
    color:#00f0ff;
    text-shadow:0 0 10px #00f0ff,0 0 20px #00f0ff;
}

.container{
    max-width:1200px;
    margin:auto;
}

/* Header */
.header{
    text-align:center;
    margin-bottom:40px;
}

/* Dashboard Grid */
.dashboard{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
    gap:25px;
}

/* Cards */
.card{
    background:#0c1224;
    padding:25px;
    border-radius:15px;
    border:1px solid #00f0ff30;
    box-shadow:0 0 15px #00f0ff20;
    text-align:center;
}

.card h3{
    color:#00f0ff;
    margin-bottom:15px;
}

/* Circular Gauge */
.gauge{
    width:160px;
    height:160px;
    border-radius:50%;
    background:conic-gradient(#00f0ff {{ confidence }}%, #1a1f3a 0%);
    display:flex;
    align-items:center;
    justify-content:center;
    margin:20px auto;
}

.gauge-inner{
    width:120px;
    height:120px;
    border-radius:50%;
    background:#050816;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
    font-weight:bold;
    color:#00f0ff;
}

/* Risk Badge */
.risk{
    padding:8px 15px;
    border-radius:20px;
    display:inline-block;
    margin-top:15px;
    font-weight:bold;
}

.high{
    background:#ff004c;
    color:white;
    box-shadow:0 0 15px #ff004c;
}

.medium{
    background:#ffae00;
    color:black;
    box-shadow:0 0 15px #ffae00;
}

.low{
    background:#00ff9c;
    color:black;
    box-shadow:0 0 15px #00ff9c;
}

/* Summary */
.summary{
    margin-top:40px;
    padding:25px;
    background:#0c1224;
    border-radius:15px;
    border-left:4px solid #00f0ff;
}

/* Video Section */
.video-section{
    margin-top:50px;
    text-align:center;
}

.video-container{
    width:700px;
    max-width:100%;
    height:400px;
    margin:20px auto;
    border-radius:15px;
    overflow:hidden;
    border:2px solid #00f0ff;
    box-shadow:0 0 25px #00f0ff40;
}

.video-container video{
    width:100%;
    height:100%;
    object-fit:cover;
}

/* Flash Background if Accident */
.alert-flash{
    animation:flash 1s infinite alternate;
}

@keyframes flash{
    from{background:#050816;}
    to{background:#1a0008;}
}

/* Buttons */
.buttons{
    margin-top:40px;
    text-align:center;
}

.btn{
    padding:12px 25px;
    border-radius:30px;
    border:none;
    font-size:14px;
    background:linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    cursor:pointer;
    margin:10px;
    text-decoration:none;
}

.btn:hover{
    transform:scale(1.05);
}

</style>
</head>

<body class="{% if 'Accident' in result %}alert-flash{% endif %}">

<div class="container">

<div class="header">
    <h1 class="neon-text">🚨 AI Accident Detection Report</h1>
</div>

<div class="dashboard">

    <!-- Confidence Gauge -->
    <div class="card">
        <h3>Confidence Level</h3>
        <div class="gauge">
            <div class="gauge-inner">
                {{ confidence }}%
            </div>
        </div>
    </div>

    <!-- Frame Stats -->
    <div class="card">
        <h3>Frame Analysis</h3>
        <p>Total Frames: {{ total_frames }}</p>
        <p>Accident Frames: {{ accident_frames }}</p>
        <p>Processing Time: {{ processing_time }} sec</p>
    </div>

    <!-- Location & Risk -->
    <div class="card">
        <h3>Location</h3>
        <p>{{ location }}</p>

        {% set risk_level = 'Low' %}
        {% if confidence > 70 %}
            {% set risk_level = 'High' %}
        {% elif confidence > 40 %}
            {% set risk_level = 'Medium' %}
        {% endif %}

        <div class="risk 
            {% if risk_level == 'High' %}high
            {% elif risk_level == 'Medium' %}medium
            {% else %}low{% endif %}">
            Risk Level: {{ risk_level }}
        </div>
    </div>

</div>

<!-- Summary -->
<div class="summary">
    <h3 class="neon-text">Incident Summary</h3>
    <p>
        {% if 'Accident' in result %}
            High probability accident detected at {{ location }}.
            System confidence is {{ confidence }}%.
            Immediate attention recommended.
        {% else %}
            No significant accident patterns detected at {{ location }}.
            System confidence indicates safe conditions.
        {% endif %}
    </p>
</div>

<!-- Video -->
<div class="video-section">
    <h3 class="neon-text">Analyzed Video</h3>

    <div class="video-container">
        <video controls>
            <source src="{{ url_for('uploaded_file', filename=video_file) }}">
        </video>
    </div>
</div>

<!-- Buttons -->
<div class="buttons">
    <a href="/" class="btn">Analyze Another Video</a>

    <a href="/download_report?result={{ result }}&confidence={{ confidence }}&location={{ location }}&total_frames={{ total_frames }}&accident_frames={{ accident_frames }}&processing_time={{ processing_time }}" 
       class="btn">Download PDF Report</a>
</div>

</div>

</body>
</html>
```
## History.html

```
<!DOCTYPE html>
<html>
<head>
<title>Accident History</title>
<style>
body{
    background:#0f172a;
    color:white;
    font-family:Poppins;
    padding:40px;
}
table{
    width:100%;
    border-collapse:collapse;
}
th,td{
    padding:12px;
    border-bottom:1px solid #334155;
    text-align:center;
}
th{
    background:#1e293b;
}
a{color:#38bdf8;text-decoration:none;}
</style>
</head>
<body>

<h2>🚨 Accident Detection History</h2>

<table>
<tr>
    <th>ID</th>
    <th>Result</th>
    <th>Confidence (%)</th>
    <th>Location</th>
    <th>Processing Time</th>
    <th>Date & Time</th>
</tr>

{% for row in records %}
<tr>
    <td>{{ row[0] }}</td>
    <td>{{ row[1] }}</td>
    <td>{{ row[2] }}</td>
    <td>{{ row[3] }}</td>
    <td>{{ row[4] }}</td>
    <td>{{ row[5] }}</td>
</tr>
{% endfor %}

</table>

<br><br>
<a href="/">Back to Home</a>

</body>
</html>
```
---

## Output :
# Home page

<img width="1657" height="886" alt="Home page" src="https://github.com/user-attachments/assets/0e60978b-8966-4bf2-a6cd-a9a8c1f8f019" />

# Result page

<img width="1916" height="1078" alt="Result1 page" src="https://github.com/user-attachments/assets/0bf31b77-30b8-49fb-a3eb-357e80ea22d6" />

# Model Acuuracy page
<img width="1917" height="1078" alt="Result page" src="https://github.com/user-attachments/assets/d3eaee9a-3aa5-496e-b45b-e80c956839c8" />

# Analysis Details 

<img width="1913" height="840" alt="Details page" src="https://github.com/user-attachments/assets/66bf1dc1-2b1b-488d-914c-2ab78500d45f" />

---
# Result

AccidentGuard is a video-based accident detection system that analyzes traffic videos to automatically detect accidents using computer vision and machine learning.  
Users can upload MP4 videos through a web interface, and the system processes frames to show real-time accident detection results.  
The output clearly indicates 🚨 Accident Detected or ✅ No Accident, with optional charts showing model performance.







