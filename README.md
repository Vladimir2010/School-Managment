# EduGrade 9 - School Management System

EduGrade 9 is a professional, full-featured online system for managing students, grades, and absences.

## Features
- **Authentication**: secure login/logout with role-based access control (Admin, Teacher, Student).
- **Student Management**: Full CRUD operations for student records.
- **Academic Tracking**: Add and manage grades (2-6 scale) with automatic GPA calculation.
- **Attendance**: Log and categorize absences as excused or unexcused.
- **Analytics**: Beautiful dashboard with Chart.js showing academic trends and attendance.
- **Reporting**: Generate professional PDF report cards for students.

## Technologies
- **Backend**: Python 3, Flask, SQLAlchemy, SQLite, Flask-Login, Flask-WTF.
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Chart.js.

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Seed the Database**:
   Initializes the database with an admin user, subjects, and sample students.
   ```bash
   python seed.py
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the system at `http://127.0.0.1:5000`.

## Default Accounts
- **Admin**: `admin` / `admin123`
- **Teacher**: `teacher1` / `teacher123`

## Project Structure
- `app.py`: Entry point and app factory.
- `models.py`: Database schema definitions.
- `routes/`: Blueprint-based implementation of modules.
- `templates/`: Jinja2 templates for the UI.
- `static/`: CSS and Client-side JS.
- `seed.py`: Database initialization script.
