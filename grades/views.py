from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Max, Min, Count
from .models import Grade
from .forms import GradeForm
from students.models import Student


def grade_list(request):
    subject = request.GET.get('subject', '')
    exam_type = request.GET.get('exam_type', '')
    class_name = request.GET.get('class_name', '')

    grades = Grade.objects.select_related('student').all()
    if subject:
        grades = grades.filter(subject__icontains=subject)
    if exam_type:
        grades = grades.filter(exam_type=exam_type)
    if class_name:
        grades = grades.filter(student__class_name=class_name)

    subjects = Grade.objects.values_list('subject', flat=True).distinct()
    classes = Student.objects.values_list('class_name', flat=True).distinct()

    # Stats
    stats = grades.aggregate(avg=Avg('marks_obtained'), mx=Max('marks_obtained'), mn=Min('marks_obtained'))

    context = {
        'grades': grades,
        'subject': subject,
        'exam_type': exam_type,
        'class_filter': class_name,
        'subjects': subjects,
        'classes': classes,
        'stats': stats,
    }
    return render(request, 'grades/list.html', context)


def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save()
            messages.success(request, f'Grade added for {grade.student.full_name}!')
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'grades/form.html', {'form': form, 'title': 'Add Grade'})


def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated!')
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'grades/form.html', {'form': form, 'title': 'Edit Grade', 'grade': grade})


def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted.')
        return redirect('grade_list')
    return render(request, 'grades/confirm_delete.html', {'grade': grade})


def student_grades(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    grades = Grade.objects.filter(student=student).order_by('-exam_date')
    subjects = grades.values('subject').annotate(avg=Avg('marks_obtained')).order_by('subject')
    overall_avg = grades.aggregate(avg=Avg('marks_obtained'))['avg']

    context = {
        'student': student,
        'grades': grades,
        'subjects': subjects,
        'overall_avg': round(overall_avg, 1) if overall_avg else 0,
    }
    return render(request, 'grades/student.html', context)
