import sqlite3
import os

DB_DIR = 'data'
DB_FILE = 'todo.db'
DATABASE = os.path.join(DB_DIR, DB_FILE)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    
    # Проверяем, существует ли таблица tasks
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    table_exists = cursor.fetchone() is not None
    
    if not os.path.exists(DATABASE):
        conn = get_db()
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("База данных инициализирована")

def get_all_tasks():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(task) for task in tasks]

def create_task(title):
    conn = get_db()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    task_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return get_task(task_id)

def get_task(task_id):
    conn = get_db()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return dict(task) if task else None

def update_task(task_id, completed):
    conn = get_db()
    conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
    conn.commit()
    conn.close()
    return get_task(task_id)

def delete_task(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return True