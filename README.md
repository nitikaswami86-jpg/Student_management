# 🎓 EduManage — Student Management System

A full-stack web application built with **Django** and **Bootstrap 5** to manage student records, attendance, and grades.

---

## 📸 Features

### Students Module
- ✅ Add, edit, delete, and search students
- ✅ Student profiles with personal, academic & guardian info
- ✅ Status tracking (Active / Inactive / Graduated)
- ✅ Filter by class, section, and status

### Attendance Module
- ✅ Mark individual student attendance
- ✅ Bulk attendance marking by class (Present / Absent / Late / Excused)
- ✅ Date-wise attendance view with statistics
- ✅ Per-student attendance report with percentage

### Grades Module
- ✅ Add grades for multiple exam types (Midterm, Final, Quiz, Assignment, Practical)
- ✅ Auto-calculates letter grade (A+, A, B+, … F) from marks
- ✅ Per-student grade report with subject-wise averages
- ✅ Filter grades by subject, exam type, class

### Dashboard
- ✅ Live statistics: total students, active, present today, avg grade
- ✅ Recent student list with quick links
- ✅ Quick action buttons

### UI / Design
- ✅ Responsive Bootstrap 5 layout
- ✅ Fixed sidebar navigation
- ✅ Colour-coded stat cards, badges, progress bars
- ✅ Mobile-friendly (collapsible sidebar)
- ✅ Django admin panel included

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip

### 2. Clone / Extract
```bash
unzip student_management_system.zip
cd student_management_system
```

### 3. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (for Admin Panel)
```bash
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)
```bash
python seed_data.py
```
This creates 12 demo students with 30 days of attendance and multiple grade records.

### 8. Run the Server
```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
student_management_system/
│
├── manage.py                  # Django entry point
├── settings.py                # Django settings
├── urls.py                    # Root URL configuration
├── wsgi.py                    # WSGI config
├── requirements.txt           # Python dependencies
├── seed_data.py               # Sample data loader
│
├── students/                  # Students app
│   ├── models.py              # Student model
│   ├── views.py               # CRUD views
│   ├── forms.py               # Student form
│   ├── urls.py                # Student URL routes
│   └── admin.py               # Admin registration
│
├── attendance/                # Attendance app
│   ├── models.py              # Attendance model
│   ├── views.py               # Attendance views
│   ├── forms.py               # Attendance forms
│   ├── urls.py                # Attendance URL routes
│   └── admin.py               # Admin registration
│
├── grades/                    # Grades app
│   ├── models.py              # Grade model (auto-grade calculation)
│   ├── views.py               # Grade views
│   ├── forms.py               # Grade form
│   ├── urls.py                # Grade URL routes
│   └── admin.py               # Admin registration
│
└── templates/                 # HTML templates
    ├── base.html              # Base layout (sidebar + topbar)
    ├── dashboard.html         # Dashboard page
    ├── students/
    │   ├── list.html          # Student list with search/filter
    │   ├── detail.html        # Student profile
    │   ├── form.html          # Add/Edit form
    │   └── confirm_delete.html
    ├── attendance/
    │   ├── list.html          # Attendance by date
    │   ├── form.html          # Mark single attendance
    │   ├── bulk.html          # Bulk attendance marking
    │   └── student.html       # Per-student attendance report
    └── grades/
        ├── list.html          # All grades with filters
        ├── form.html          # Add/Edit grade
        ├── student.html       # Per-student grade report
        └── confirm_delete.html
```

---

## 🌐 URL Reference

| URL | Page |
|-----|------|
| `/` | Dashboard |
| `/students/` | All Students |
| `/students/add/` | Add Student |
| `/students/<id>/` | Student Detail |
| `/students/<id>/edit/` | Edit Student |
| `/attendance/` | Attendance List |
| `/attendance/mark/` | Mark Single Attendance |
| `/attendance/bulk/` | Bulk Attendance |
| `/grades/` | Grade List |
| `/grades/add/` | Add Grade |
| `/admin/` | Django Admin Panel |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| Database | SQLite (default) |
| Frontend | Bootstrap 5.3 |
| Icons | Bootstrap Icons 1.11 |
| Fonts | DM Sans + Space Grotesk |

---

## 💡 Extending the Project

- **Switch to PostgreSQL**: Update `DATABASES` in `settings.py`
- **Add authentication**: Use `django.contrib.auth` login views
- **Export to Excel**: Add `openpyxl` and a download view
- **REST API**: Add `djangorestframework` for mobile app backend
- **Charts**: Integrate Chart.js in templates for grade analytics

---

## 📄 License

MIT License — free for personal and commercial use.
