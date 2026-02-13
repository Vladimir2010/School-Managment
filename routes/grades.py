from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, Student, Subject, Grade
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

grades_bp = Blueprint('grades', __name__)

class GradeForm(FlaskForm):
    student_id = SelectField('Ученик', coerce=int, validators=[DataRequired(message="Изберете ученик")])
    subject_id = SelectField('Предмет', coerce=int, validators=[DataRequired(message="Изберете предмет")])
    grade_value = IntegerField('Оценка (2-6)', validators=[DataRequired(message="Въведете оценка"), NumberRange(min=2, max=6, message="Оценката трябва да е между 2 и 6")])
    submit = SubmitField('Запази оценка')

@grades_bp.route('/')
@login_required
def list_grades():
    student_id = request.args.get('student_id', type=int)
    subject_id = request.args.get('subject_id', type=int)
    
    query = Grade.query
    if student_id:
        query = query.filter_by(student_id=student_id)
    if subject_id:
        query = query.filter_by(subject_id=subject_id)
        
    grades = query.order_by(Grade.date_added.desc()).all()
    students = Student.query.all()
    subjects = Subject.query.all()
    
    return render_template('grades/list.html', title='Оценки', grades=grades, students=students, subjects=subjects)

@grades_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_grade():
    if current_user.role not in ['admin', 'teacher']:
        flash('Нямате права за добавяне на оценки.')
        return redirect(url_for('grades.list_grades'))
    
    form = GradeForm()
    form.student_id.choices = [(s.id, f"{s.first_name} {s.last_name}") for s in Student.query.all()]
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    
    if form.validate_on_submit():
        grade = Grade(
            student_id=form.student_id.data,
            subject_id=form.subject_id.data,
            grade_value=form.grade_value.data
        )
        db.session.add(grade)
        db.session.commit()
        flash('Оценката беше добавена успешно!')
        return redirect(url_for('grades.list_grades'))
    return render_template('grades/form.html', form=form, title='Добавяне на оценка')
