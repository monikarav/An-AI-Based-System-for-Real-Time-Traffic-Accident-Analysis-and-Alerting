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

## core code

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

