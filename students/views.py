from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from .models import Student
from .forms import StudentForm
from attendance.models import Attendance
from grades.models import Grade
import json


def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    graduated = Student.objects.filter(status='graduated').count()
    inactive = Student.objects.filter(status='inactive').count()
    
    recent_students = Student.objects.order_by('-created_at')[:5]
    
    # Attendance summary
    from django.utils import timezone
    import datetime
    today = datetime.date.today()
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='present').count()
    absent_today = today_attendance.filter(status='absent').count()
    
    # Grade distribution
    grade_avg = Grade.objects.aggregate(avg=Avg('marks_obtained'))['avg'] or 0
    
    context = {
        'total_students': total_students,
        'active_students': active_students,
        'graduated': graduated,
        'inactive': inactive,
        'recent_students': recent_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'grade_avg': round(grade_avg, 1),
    }
    return render(request, 'dashboard.html', context)


def student_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    class_filter = request.GET.get('class_name', '')

    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(email__icontains=query)
        )
    if status:
        students = students.filter(status=status)
    if class_filter:
        students = students.filter(class_name=class_filter)

    classes = Student.objects.values_list('class_name', flat=True).distinct()
    context = {
        'students': students,
        'query': query,
        'status': status,
        'class_filter': class_filter,
        'classes': classes,
    }
    return render(request, 'students/list.html', context)


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances = Attendance.objects.filter(student=student).order_by('-date')[:10]
    grades = Grade.objects.filter(student=student).order_by('-exam_date')
    
    total_classes = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status='present').count()
    attendance_pct = round((present_count / total_classes * 100), 1) if total_classes > 0 else 0
    avg_marks = grades.aggregate(avg=Avg('marks_obtained'))['avg']
    
    context = {
        'student': student,
        'attendances': attendances,
        'grades': grades,
        'attendance_pct': attendance_pct,
        'avg_marks': round(avg_marks, 1) if avg_marks else 0,
    }
    return render(request, 'students/detail.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} added successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'students/form.html', {'form': form, 'title': 'Add Student'})


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/form.html', {'form': form, 'title': 'Edit Student', 'student': student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'Student {name} deleted.')
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'student': student})
