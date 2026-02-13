from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='student') # admin, teacher, student

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    student_class = db.Column(db.String(10), nullable=False) # e.g., '9A'
    email = db.Column(db.String(120), unique=True, index=True)
    
    grades = db.relationship('Grade', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    absences = db.relationship('Absence', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def average_grade(self):
        grades = self.grades.all()
        if not grades:
            return 0.0
        return round(sum(g.grade_value for g in grades) / len(grades), 2)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    
    grades = db.relationship('Grade', backref='subject', lazy='dynamic')

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    grade_value = db.Column(db.Integer, nullable=False) # 2-6
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Absence(db.Model):
    __tablename__ = 'absences'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date())
    type = db.Column(db.String(20), nullable=False) # excused, unexcused
