from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from .models import Attendance
from .forms import AttendanceForm, BulkAttendanceForm
from students.models import Student
import datetime


def attendance_list(request):
    date_filter = request.GET.get('date', str(datetime.date.today()))
    class_filter = request.GET.get('class_name', '')

    attendances = Attendance.objects.select_related('student').filter(date=date_filter)
    if class_filter:
        attendances = attendances.filter(student__class_name=class_filter)

    # Stats for selected date
    total = attendances.count()
    present = attendances.filter(status='present').count()
    absent = attendances.filter(status='absent').count()
    late = attendances.filter(status='late').count()

    classes = Student.objects.values_list('class_name', flat=True).distinct()

    context = {
        'attendances': attendances,
        'date_filter': date_filter,
        'class_filter': class_filter,
        'classes': classes,
        'total': total,
        'present': present,
        'absent': absent,
        'late': late,
    }
    return render(request, 'attendance/list.html', context)


def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            att = form.save(commit=False)
            existing = Attendance.objects.filter(
                student=att.student, date=att.date, subject=att.subject
            ).first()
            if existing:
                existing.status = att.status
                existing.remarks = att.remarks
                existing.save()
                messages.success(request, 'Attendance updated!')
            else:
                att.save()
                messages.success(request, 'Attendance marked!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/form.html', {'form': form, 'title': 'Mark Attendance'})


def bulk_attendance(request):
    class_name = request.GET.get('class_name', '')
    date = request.GET.get('date', str(datetime.date.today()))
    students = Student.objects.filter(status='active')
    if class_name:
        students = students.filter(class_name=class_name)

    if request.method == 'POST':
        date_val = request.POST.get('date')
        subject = request.POST.get('subject', '')
        for student in Student.objects.filter(status='active'):
            status = request.POST.get(f'status_{student.pk}', 'absent')
            Attendance.objects.update_or_create(
                student=student, date=date_val, subject=subject,
                defaults={'status': status}
            )
        messages.success(request, f'Bulk attendance saved for {date_val}!')
        return redirect('attendance_list')

    classes = Student.objects.values_list('class_name', flat=True).distinct()
    context = {
        'students': students,
        'date': date,
        'class_name': class_name,
        'classes': classes,
    }
    return render(request, 'attendance/bulk.html', context)


def student_attendance(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    total = attendances.count()
    present = attendances.filter(status='present').count()
    absent = attendances.filter(status='absent').count()
    late = attendances.filter(status='late').count()
    pct = round((present / total * 100), 1) if total > 0 else 0

    context = {
        'student': student,
        'attendances': attendances,
        'total': total,
        'present': present,
        'absent': absent,
        'late': late,
        'pct': pct,
    }
    return render(request, 'attendance/student.html', context)
