# attendance/face_cache.py
from .models import RegisteredUser
import numpy as np

def load_known_faces():
    faces = RegisteredUser.objects.all()
    known_encodings = [np.fromstring(face.encoding, sep=',') for face in faces]     
    known_names = [face.name for face in faces]
    return known_encodings, known_names

# Load once at module level (only at startup)
known_encodings, known_names = load_known_faces()