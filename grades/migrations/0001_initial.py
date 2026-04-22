from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('exam_type', models.CharField(choices=[('midterm', 'Midterm'), ('final', 'Final'), ('quiz', 'Quiz'), ('assignment', 'Assignment'), ('practical', 'Practical')], default='midterm', max_length=20)),
                ('marks_obtained', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_marks', models.DecimalField(decimal_places=2, default=100, max_digits=5)),
                ('grade', models.CharField(blank=True, choices=[('A+', 'A+ (95-100)'), ('A', 'A (90-94)'), ('A-', 'A- (85-89)'), ('B+', 'B+ (80-84)'), ('B', 'B (75-79)'), ('B-', 'B- (70-74)'), ('C+', 'C+ (65-69)'), ('C', 'C (60-64)'), ('C-', 'C- (55-59)'), ('D', 'D (50-54)'), ('F', 'F (Below 50)')], max_length=2)),
                ('exam_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='students.student')),
            ],
            options={
                'ordering': ['-exam_date'],
            },
        ),
    ]
