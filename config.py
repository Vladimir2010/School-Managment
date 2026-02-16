import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-edu-grade-9'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'edugrade9.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEACHER_REGISTRATION_KEY = os.environ.get('TEACHER_REGISTRATION_KEY') or 'spge'
