from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from models import db, Student, Grade, Absence, Subject
from sqlalchemy import func
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def dashboard():
    # Average grade by student
    avg_grades = db.session.query(
        Student.first_name, Student.last_name, func.avg(Grade.grade_value).label('average')
    ).join(Grade).group_by(Student.id).all()
    
    # Absences by class
    absences_by_class = db.session.query(
        Student.student_class, func.count(Absence.id).label('count')
    ).join(Absence).group_by(Student.student_class).all()
    
    return render_template('reports/dashboard.html', title='Справки и Анализ', avg_grades=avg_grades, absences_by_class=absences_by_class)

@reports_bp.route('/pdf/student/<int:id>')
@login_required
def student_report_pdf(id):
    student = Student.query.get_or_404(id)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Standard fonts don't support Cyrillic well. 
    # For a perfect result, we would register a .ttf font here.
    # For now, we'll use a standard font and hope for the best, 
    # but in a real app, we'd bundle a Cyrillic-capable font.
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"Служебна бележка: {student.first_name} {student.last_name}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Клас: {student.student_class}")
    p.drawString(100, 715, f"Имейл: {student.email}")
    
    p.drawString(100, 680, "Оценки:")
    y = 660
    grades = Grade.query.filter_by(student_id=id).all()
    for g in grades:
        p.drawString(120, y, f"{g.subject.name}: {g.grade_value} (Дата: {g.date_added.strftime('%d.%m.%Y')})")
        y -= 20
        
    p.drawString(100, y - 20, "Отсъствия:")
    y -= 40
    absences = Absence.query.filter_by(student_id=id).all()
    for a in absences:
        type_bg = "Извинено" if a.type == 'excused' else "Неизвинено"
        p.drawString(120, y, f"{a.date.strftime('%d.%m.%Y')} - {type_bg}")
        y -= 20

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"report_{student.last_name}.pdf", mimetype='application/pdf')
