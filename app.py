from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import database

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # За сесиите (login)

# Свързване с базата данни при всяка заявка
@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

def get_db():
    return database.get_db()

# --- МАРШРУТИ (ROUTES) ---

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверка в базата данни
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Грешно потребителско име.'
        elif user['password'] != password:
            error = 'Грешна парола.'
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/students')
def students():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    all_students = db.execute('SELECT * FROM students').fetchall()
    return render_template('students.html', students=all_students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['class']
        
        db = get_db()
        db.execute('INSERT INTO students (name, student_class) VALUES (?, ?)',
                   (name, student_class))
        db.commit()
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

@app.route('/grades')
def grades():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    # Взимаме оценките + имената на учениците (JOIN)
    query = '''
        SELECT grades.id, students.name, grades.subject, grades.grade, grades.date_added
        FROM grades
        JOIN students ON grades.student_id = students.id
        ORDER BY grades.date_added DESC
    '''
    all_grades = db.execute(query).fetchall()
    return render_template('grades.html', grades=all_grades)

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()

    if request.method == 'POST':
        student_id = request.form['student_id']
        subject = request.form['subject']
        grade = request.form['grade']
        
        db.execute('INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)',
                   (student_id, subject, grade))
        db.commit()
        return redirect(url_for('grades'))
    
    students = db.execute('SELECT * FROM students').fetchall()
    return render_template('add_grade.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
