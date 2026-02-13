from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, Student, Absence
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

absences_bp = Blueprint('absences', __name__)

class AbsenceForm(FlaskForm):
    student_id = SelectField('Ученик', coerce=int, validators=[DataRequired(message="Изберете ученик")])
    date = DateField('Дата', default=datetime.utcnow, validators=[DataRequired(message="Въведете дата")])
    type = SelectField('Вид', choices=[('excused', 'Извинено'), ('unexcused', 'Неизвинено')], validators=[DataRequired(message="Изберете вид")])
    submit = SubmitField('Запиши отсъствие')

@absences_bp.route('/')
@login_required
def list_absences():
    student_id = request.args.get('student_id', type=int)
    query = Absence.query
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    absences = query.order_by(Absence.date.desc()).all()
    students = Student.query.all()
    return render_template('absences/list.html', title='Отсъствия', absences=absences, students=students)

@absences_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_absence():
    if current_user.role not in ['admin', 'teacher']:
        flash('Нямате права за отразяване на отсъствия.')
        return redirect(url_for('absences.list_absences'))
    
    form = AbsenceForm()
    form.student_id.choices = [(s.id, f"{s.first_name} {s.last_name}") for s in Student.query.all()]
    
    if form.validate_on_submit():
        absence = Absence(
            student_id=form.student_id.data,
            date=form.date.data,
            type=form.type.data
        )
        db.session.add(absence)
        db.session.commit()
        flash('Отсъствието беше записано успешно!')
        return redirect(url_for('absences.list_absences'))
    return render_template('absences/form.html', form=form, title='Запис на отсъствие')
