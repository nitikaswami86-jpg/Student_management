from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('bulk/', views.bulk_attendance, name='bulk_attendance'),
    path('student/<int:student_pk>/', views.student_attendance, name='student_attendance'),
]
