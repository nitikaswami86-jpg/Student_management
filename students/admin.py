from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'email', 'class_name', 'section', 'status']
    list_filter = ['status', 'gender', 'class_name']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']
