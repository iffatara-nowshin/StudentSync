# StudentSync 🎓

A full-stack Student Management System built with **Django** + **SQLite**, featuring a purple-gradient
glassmorphic dashboard, animated UI, student/course CRUD, attendance tracking, and results.

## Features

- 🔐 Login-protected dashboard (Django auth)
- 📊 Animated dashboard with live stat counters + doughnut chart (Chart.js)
- 🧑‍🎓 Full Student CRUD (add / edit / view / delete, with photo upload)
- 📚 Course management
- 🗓 Daily attendance marking + attendance history report
- 📈 Per-student exam results with progress bars
- 🎨 Purple gradient theme with glass cards, animated background blobs, and micro-interactions
- 📱 Responsive layout with a collapsible sidebar on mobile

## Tech Stack

- **Backend:** Django 5 (function-based views, class-based login view)
- **Database:** SQLite (zero config — swap for Postgres/MySQL later if you want)
- **Frontend:** Django templates + vanilla CSS/JS + Chart.js (via CDN)

---

## 1. Prerequisites

- Python 3.10+ installed
- pip

Check your Python version:
```bash
python --version
```

## 2. Setup

Unzip the project, then open a terminal inside the `studentSync` folder.

**Create a virtual environment (recommended):**
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## 3. Set up the database

```bash
python manage.py migrate
```

This creates `db.sqlite3` with all tables (Students, Courses, Attendance, Results) using the
migration already included in the project — no extra steps needed.

## 4. Create your admin/login account

```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password). This is the account you'll use to log in.

## 5. Run the server

```bash
python manage.py runserver
```

Open your browser at:
- **App:** http://127.0.0.1:8000/  (log in with the superuser you just created)
- **Django Admin:** http://127.0.0.1:8000/admin/

## 6. Using StudentSync

1. Log in with your superuser credentials.
2. Go to **Courses** → add a course (e.g. "Computer Science", code `CSE-101`).
3. Go to **Students** → add students and assign them to a course. You can attach a photo too.
4. Go to **Attendance** → pick a date/course and mark students Present/Absent.
5. Open any student's profile to add exam **Results** and see their attendance history.
6. The **Dashboard** updates automatically with live totals and a course-distribution chart.

---

## Project Structure

```
studentSync/
├── manage.py
├── requirements.txt
├── db.sqlite3                  ← created after migrate
├── studentSync/                ← project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── students/                   ← main app
    ├── models.py                (Course, Student, Attendance, Result)
    ├── views.py                 (dashboard + all CRUD views)
    ├── forms.py
    ├── urls.py
    ├── admin.py
    ├── templatetags/
    ├── templates/
    │   ├── base.html            (sidebar + theme shell)
    │   └── students/            (dashboard, list, forms, etc.)
    └── static/students/
        ├── css/style.css        (purple gradient theme)
        └── js/script.js         (sidebar toggle, animations)
```

## Notes & Next Steps

- `DEBUG = True` and `SECRET_KEY` in `studentSync/settings.py` are set for local development only —
  change both before deploying anywhere public.
- Uploaded student photos are stored in `/media/student_photos/`.
- To switch to PostgreSQL/MySQL later, just update the `DATABASES` setting in `settings.py` and
  re-run `python manage.py migrate`.
- Want more features (bulk CSV import, email notifications, fee management, timetable)? Just ask —
  the codebase is intentionally kept simple and easy to extend.

Enjoy StudentSync! ✨
