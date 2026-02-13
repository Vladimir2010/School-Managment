from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, Student
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

students_bp = Blueprint('students', __name__)

class StudentForm(FlaskForm):
    first_name = StringField('Име', validators=[DataRequired(message="Задължително поле")])
    last_name = StringField('Фамилия', validators=[DataRequired(message="Задължително поле")])
    student_class = StringField('Клас', validators=[DataRequired(message="Задължително поле")])
    email = StringField('Имейл', validators=[DataRequired(message="Задължително поле"), Email(message="Невалиден имейл")])
    submit = SubmitField('Запази')

@students_bp.route('/')
@login_required
def list_students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = Student.query
    if search:
        query = query.filter(
            (Student.first_name.ilike(f'%{search}%')) | 
            (Student.last_name.ilike(f'%{search}%'))
        )
    students = query.order_by(Student.last_name.asc()).paginate(page=page, per_page=10)
    return render_template('students/list.html', title='Списък с ученици', students=students, search=search)

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role not in ['admin', 'teacher']:
        flash('Нямате права за тази операция.')
        return redirect(url_for('students.list_students'))
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            student_class=form.student_class.data,
            email=form.email.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Ученикът беше добавен успешно!')
        return redirect(url_for('students.list_students'))
    return render_template('students/form.html', form=form, title='Добавяне на ученик')

@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if current_user.role not in ['admin', 'teacher']:
        flash('Нямате права за тази операция.')
        return redirect(url_for('students.list_students'))
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.student_class = form.student_class.data
        student.email = form.email.data
        db.session.commit()
        flash('Данните бяха обновени успешно!')
        return redirect(url_for('students.list_students'))
    return render_template('students/form.html', form=form, title='Редактиране на ученик')

@students_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    if current_user.role != 'admin':
        flash('Само администратори могат да трият записи.')
        return redirect(url_for('students.list_students'))
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Записът беше изтрит.')
    return redirect(url_for('students.list_students'))
