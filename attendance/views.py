from django.shortcuts import render, HttpResponse
import numpy as np
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import face_recognition as fc
import json
import base64
from PIL import Image
from io import BytesIO
from .models import RegisteredUser, Attendace
from django.utils.timezone import localtime
import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')

def webcam_view(request):
    return render(request, 'register.html')

def detect(request):
    return render(request, 'detect.html')

@csrf_exempt
def register_face(request):
    if request.method == 'POST':
        try:
            print("=== Request received ===")
            data = json.loads(request.body)
            name = data.get('name')
            image_data = data.get('image')

            print("Name:", name)
            print("Image data starts with:", image_data[:30] if image_data else "None")

            if not name or not image_data:
                return JsonResponse({'error': 'Missing data'}, status=400)

            # Clean image
            if "," in image_data:
                image_data = image_data.split(',')[1]
            decoded_image = base64.b64decode(image_data)
            image = Image.open(BytesIO(decoded_image))
            image_np = np.array(image)

            print("Image shape:", image_np.shape)

            # Extract face encoding
            face_encodings = fc.face_encodings(image_np)
    
            if not face_encodings:
                return JsonResponse({'error': 'No face found'}, status=400)
            encoding = face_encodings[0]
            encoding_b64 = base64.b64encode(encoding.tobytes()).decode('utf-8')


            RegisteredUser.objects.create(name=name, encoding=encoding_b64)

            return JsonResponse({'message': f'Face registered for {name}'})
        except Exception as e:
            print("Error occurred:", str(e))  
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def detect_face(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            if not image_data:
                return JsonResponse({'success': False, 'error': 'No image data provided'})

            # Decode the base64 image
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes)).convert('RGB')
            np_image = np.array(image)

            # Extract encoding from the input image
            face_encodings = fc.face_encodings(np_image)
            if not face_encodings:
                return JsonResponse({'success': False, 'error': 'No face detected'})

            face_encoding = face_encodings[0]

            # Load known faces
            known_faces = RegisteredUser.objects.all()
            known_encodings = [
                np.frombuffer(base64.b64decode(f.encoding), dtype=np.float64)
                for f in known_faces
            ]
            known_names = [f.name for f in known_faces]

            matches = fc.compare_faces(known_encodings, face_encoding)
            print(matches)
            if True in matches:
                matched_index = matches.index(True)
                matched_name = known_names[matched_index]
                return JsonResponse({'success': True, 'name': matched_name})
            else:
                return JsonResponse({'success': False, 'error': 'Face not recognized'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# def detect_face(request):
#     if request.method == 'POST':
#         try:
#             data = json.load(request.body)
#             image_data = data.get('image')
#             image_data = image_data.split(',')[1]
#             decoded = base64.b64decode(image_data)
#             image = Image.open(BytesIO(decoded))
#             image_np = np.array(image)
#             # captured image encoding
#             unknown_encoding = fc.face_encodings(image_np)
#             if not unknown_encoding:
#                 return JsonResponse({'match_found':False})
#             unknown_encoding = unknown_encoding[0]

#             # Compare with stored encodings
#             matches = fc.compare_faces(known_encodings, unknown_encoding)
#             name = "Unknown"
#             if np.any(matches):
#                 first_match_index = np.armax(matches)
#                 name = known_names[first_match_index]
#             return JsonResponse({'name':name})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def confirm_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            now = datetime.datetime.now()
            Attendace.objects.create(name=name, timestamp=now)
            return JsonResponse({'message': f'Attendance recorded for {name}'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def attendance_list(request):
    records = Attendace.objects.all().order_by('-timestamp')
    for r in records:
        r.local_time = localtime(r.timestamp)  # optional: show in local time
    return render(request, 'attendanceList.html', {'records': records})