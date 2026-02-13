from app import app
from models import db, User, Student, Subject, Grade, Absence
from datetime import datetime, date
import random

def seed_data():
    with app.app_context():
        # Clear existing data for fresh start
        db.drop_all()
        db.create_all()

        # Users
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        teacher = User(username='teacher1', role='teacher')
        teacher.set_password('teacher123')
        db.session.add(teacher)

        teacher2 = User(username='teacher2', role='teacher')
        teacher2.set_password('teacher123')
        db.session.add(teacher2)

        teacher3 = User(username='teacher3', role='teacher')
        teacher3.set_password('teacher123')
        db.session.add(teacher3)

        # Subjects
        subjects = ['Математика', 'Физика', 'История', 'Биология', 'Химия', 'Английски език', 'Информатика', 'География']
        subject_objects = []
        for sub_name in subjects:
            s = Subject(name=sub_name)
            db.session.add(s)
            subject_objects.append(s)

        # Students
        students_data = [
            ('Иван', 'Иванов', '9А', 'ivan@school.bg'),
            ('Мария', 'Петрова', '9А', 'maria@school.bg'),
            ('Георги', 'Димитров', '9Б', 'georgi@school.bg'),
            ('Елена', 'Стоянова', '9Б', 'elena@school.bg'),
            ('Николай', 'Колев', '9В', 'nikolay@school.bg'),
            ('Стефан', 'Ангелов', '9В', 'stefan@school.bg')
        ]
        
        student_objects = []
        for f, l, c, e in students_data:
            s = Student(first_name=f, last_name=l, student_class=c, email=e)
            db.session.add(s)
            student_objects.append(s)

        db.session.commit()

        # Add some random grades and absences
        for s in student_objects:
            # 5 random grades
            for _ in range(5):
                db.session.add(Grade(
                    student_id=s.id,
                    subject_id=random.choice(subject_objects).id,
                    grade_value=random.randint(3, 6)
                ))
            # 2 random absences
            for _ in range(2):
                db.session.add(Absence(
                    student_id=s.id,
                    date=date(2026, 2, random.randint(1, 10)),
                    type=random.choice(['excused', 'unexcused'])
                ))

        db.session.commit()
        print("Базата данни е захранена успешно с български данни!")

if __name__ == '__main__':
    seed_data()
