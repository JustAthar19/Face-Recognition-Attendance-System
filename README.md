# Face Recognition Attendance System (Retro Style)

A web-based face recognition attendance system built with Django, OpenCV, and face_recognition — featuring a retro pixel-art UI with real-time webcam detection and attendance logging.


---
## Features
-  Register faces through webcam
-  Real-time face detection and recognition
-  Popup confirmation for marking attendance
-  Attendance logging with timestamps
---
## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Face Detection:** `face_recognition` (dlib + OpenCV)
- **Database:** SQLite
- **Style:** Retro pixel design using [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P)
---
## Screenshots

- Register data 
- Face Recognition 
- Mark Attendance 
- Show Attendance Record 
--- 
🚧 Work in Progress
This project is actively being developed. Upcoming features include:
- 🔒 Face liveness detection (anti-spoofing)
- 👤 Admin dashboard 
- 📊 Export attendance data to CSV or Excel
- 📆 Data Filtering
---

## 🔧 Setup Instructions

```bash
git clone https://github.com/JustAthar19/Face-Recognition-Attendance-System.git
cd face-recognition-attendance-system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
