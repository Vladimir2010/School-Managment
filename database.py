import sqlite3
from flask import g

DATABASE = 'school.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    print("Инициализиране на базата данни...")
    with sqlite3.connect(DATABASE) as db:
        with open('schema.sql', encoding='utf-8') as f:
            db.executescript(f.read())
    print("Базата данни е готова!")

if __name__ == '__main__':
    init_db()
