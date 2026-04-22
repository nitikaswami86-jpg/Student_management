#!/usr/bin/env python
"""
Run this script to populate the database with sample data.
Usage: python seed_data.py
"""
import os, sys, django, random, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from students.models import Student
from attendance.models import Attendance
from grades.models import Grade

CLASSES = ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
SECTIONS = ['A', 'B', 'C']
SUBJECTS = ['Mathematics', 'Physics', 'Chemistry', 'English', 'History', 'Biology', 'Computer Science']
EXAM_TYPES = ['midterm', 'final', 'quiz', 'assignment']

STUDENTS_DATA = [
    ('Aarav', 'Sharma', 'aarav.sharma@school.edu', '9876543210', 'M'),
    ('Priya', 'Singh', 'priya.singh@school.edu', '9876543211', 'F'),
    ('Rahul', 'Verma', 'rahul.verma@school.edu', '9876543212', 'M'),
    ('Ananya', 'Gupta', 'ananya.gupta@school.edu', '9876543213', 'F'),
    ('Vikram', 'Kumar', 'vikram.kumar@school.edu', '9876543214', 'M'),
    ('Sneha', 'Patel', 'sneha.patel@school.edu', '9876543215', 'F'),
    ('Arjun', 'Reddy', 'arjun.reddy@school.edu', '9876543216', 'M'),
    ('Kavya', 'Nair', 'kavya.nair@school.edu', '9876543217', 'F'),
    ('Rohan', 'Joshi', 'rohan.joshi@school.edu', '9876543218', 'M'),
    ('Divya', 'Mehta', 'divya.mehta@school.edu', '9876543219', 'F'),
    ('Karan', 'Agarwal', 'karan.agarwal@school.edu', '9876543220', 'M'),
    ('Pooja', 'Malhotra', 'pooja.malhotra@school.edu', '9876543221', 'F'),
]

print("Creating students...")
students = []
for i, (first, last, email, phone, gender) in enumerate(STUDENTS_DATA, 1):
    s, created = Student.objects.get_or_create(
        student_id=f'STU2024{i:03d}',
        defaults={
            'first_name': first, 'last_name': last,
            'email': email, 'phone': phone,
            'gender': gender,
            'class_name': random.choice(CLASSES),
            'section': random.choice(SECTIONS),
            'status': 'active',
            'date_of_birth': datetime.date(2006, random.randint(1,12), random.randint(1,28)),
            'guardian_name': f'Mr./Mrs. {last}',
            'guardian_phone': f'98765{random.randint(10000,99999)}',
        }
    )
    students.append(s)
    if created: print(f"  ✓ {s.full_name}")

print("\nCreating attendance records...")
today = datetime.date.today()
for student in students:
    for days_ago in range(30, 0, -1):
        date = today - datetime.timedelta(days=days_ago)
        if date.weekday() < 5:  # weekdays only
            r = random.random()
            status = 'present' if r > 0.15 else ('absent' if r > 0.05 else 'late')
            Attendance.objects.get_or_create(
                student=student, date=date, subject='',
                defaults={'status': status}
            )
print("  ✓ Attendance created for last 30 days")

print("\nCreating grade records...")
for student in students:
    for subject in random.sample(SUBJECTS, 4):
        for exam_type in random.sample(EXAM_TYPES, 2):
            marks = random.randint(45, 100)
            Grade.objects.get_or_create(
                student=student, subject=subject, exam_type=exam_type,
                defaults={
                    'marks_obtained': marks,
                    'total_marks': 100,
                    'exam_date': today - datetime.timedelta(days=random.randint(1, 60)),
                }
            )
print("  ✓ Grade records created")

print("\n✅ Sample data loaded successfully!")
print(f"   Students: {Student.objects.count()}")
print(f"   Attendance: {Attendance.objects.count()}")
print(f"   Grades: {Grade.objects.count()}")
