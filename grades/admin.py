from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'marks_obtained', 'total_marks', 'grade', 'exam_date']
    list_filter = ['exam_type', 'grade', 'subject']
    search_fields = ['student__first_name', 'student__last_name', 'subject']
