from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username = StringField('Потребителско име', validators=[DataRequired(message="Задължително поле")])
    password = PasswordField('Парола', validators=[DataRequired(message="Задължително поле")])
    remember_me = BooleanField('Запомни ме')
    submit = SubmitField('Влез')

class RegistrationForm(FlaskForm):
    username = StringField('Потребителско име', validators=[DataRequired(message="Задължително pole")])
    password = PasswordField('Парола', validators=[DataRequired(message="Задължително pole")])
    role = SelectField('Роля', choices=[('student', 'Ученик'), ('teacher', 'Учител')], validators=[DataRequired()])
    teacher_key = StringField('Ключ за учител')
    submit = SubmitField('Регистрирай се')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Грешно потребителско име или парола')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    return render_template('auth/login.html', title='Вход', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Потребителското име вече е заето.')
            return redirect(url_for('auth.register'))
        
        # Check teacher registration key
        if form.role.data == 'teacher':
            from flask import current_app
            if form.teacher_key.data != current_app.config['TEACHER_REGISTRATION_KEY']:
                flash('Невалиден ключ за учител!')
                return redirect(url_for('auth.register'))
                
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрацията беше успешна! Вече можете да влезете.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)
