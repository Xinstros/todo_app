from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

# Initialize database
def init_db():
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                priority TEXT DEFAULT 'low',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)

# Run init_db when app starts
with app.app_context():
    init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT id, text, priority, created_at FROM tasks ORDER BY created_at DESC")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)
   
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (text) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        print(f"Task added to database: {task}")
    except Error as e:
        print(f"Error: {e}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)