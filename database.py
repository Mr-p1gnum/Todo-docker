import os
import psycopg2
import psycopg2.extras

def get_db():
    """Возвращает соединение с PostgreSQL. Параметры берутся из переменных окружения."""
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "todo"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn

def init_db():
    """Создаёт таблицу, если её нет."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()
    conn.close()
    print("База данных инициализирована")

def get_all_tasks():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = cur.fetchall()
    conn.close()
    return [dict(task) for task in tasks]

def create_task(title):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING id", 
            (title,)
        )
        task_id = cur.fetchone()['id']
        conn.commit()
    conn.close()
    return get_task(task_id)

def get_task(task_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        task = cur.fetchone()
    conn.close()
    return dict(task) if task else None

def update_task(task_id, completed):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('UPDATE tasks SET completed = %s WHERE id = %s', (completed, task_id))
        conn.commit()
    conn.close()
    return get_task(task_id)

def delete_task(task_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
    conn.close()
    return True