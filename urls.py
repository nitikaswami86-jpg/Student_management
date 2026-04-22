from django.contrib import admin
from django.urls import path, include
from students import views as student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', student_views.dashboard, name='dashboard'),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('grades/', include('grades.urls')),
]
