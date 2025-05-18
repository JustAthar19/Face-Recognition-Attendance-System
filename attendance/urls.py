from django.urls import path
from . import views

urlpatterns=[
    # path("", views.webcam_view, name='webcam'),
    path("", views.home, name='home'),
    path("register/", views.webcam_view, name='register'),
    path('register_face/', views.register_face, name='register face'),
    path('detect/', views.detect, name='webcam detect'),
    path('detect_face/', views.detect_face, name='detect_face'),
    path('mark_attendance/', views.confirm_attendance, name='confirm'),
    path('attendance/', views.attendance_list, name='attendance list')
]