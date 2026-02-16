from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db, User
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login = LoginManager(app)
    login.login_view = 'auth.login'
    csrf = CSRFProtect(app)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.grades import grades_bp
    from routes.absences import absences_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(grades_bp, url_prefix='/grades')
    app.register_blueprint(absences_bp, url_prefix='/absences')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    @app.route('/')
    def index():
        return render_template('index.html', title='Начало')

    @app.route('/project')
    def project():
        return render_template('project.html', title='Проект и Курсова работа')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html', title='Страницата не е намерена'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html', title='Системна грешка'), 500

    # Logging setup
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/edugrade9.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('EduGrade 9 стартира')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
