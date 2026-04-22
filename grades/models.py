from django.db import models
from students.models import Student


class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (95-100)'), ('A', 'A (90-94)'), ('A-', 'A- (85-89)'),
        ('B+', 'B+ (80-84)'), ('B', 'B (75-79)'), ('B-', 'B- (70-74)'),
        ('C+', 'C+ (65-69)'), ('C', 'C (60-64)'), ('C-', 'C- (55-59)'),
        ('D', 'D (50-54)'), ('F', 'F (Below 50)'),
    ]
    EXAM_TYPES = [
        ('midterm', 'Midterm'), ('final', 'Final'), ('quiz', 'Quiz'),
        ('assignment', 'Assignment'), ('practical', 'Practical'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='midterm')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    exam_date = models.DateField()
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return f"{self.student.full_name} - {self.subject} - {self.grade}"

    def save(self, *args, **kwargs):
        # Auto-calculate grade
        pct = (self.marks_obtained / self.total_marks) * 100
        if pct >= 95: self.grade = 'A+'
        elif pct >= 90: self.grade = 'A'
        elif pct >= 85: self.grade = 'A-'
        elif pct >= 80: self.grade = 'B+'
        elif pct >= 75: self.grade = 'B'
        elif pct >= 70: self.grade = 'B-'
        elif pct >= 65: self.grade = 'C+'
        elif pct >= 60: self.grade = 'C'
        elif pct >= 55: self.grade = 'C-'
        elif pct >= 50: self.grade = 'D'
        else: self.grade = 'F'
        super().save(*args, **kwargs)

    @property
    def percentage(self):
        return round((self.marks_obtained / self.total_marks) * 100, 1)
