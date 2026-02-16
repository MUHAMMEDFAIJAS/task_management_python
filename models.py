from db import connect
import bcrypt
from db import connect


def create_tables():
    conn = connect()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    
    # Tasks table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()



def create_user(username, password):
    conn = connect()
    cur = conn.cursor()

    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()



def get_user_by_username(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user


def  create_task(title,user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title, user_id) VALUES (?, ?)",
        (title, user_id)
    )
    conn.commit()
    conn.close()


def get_tasks_by_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cur.fetchall()
    conn.close()
    return tasks  


def update_task(task_id, title,user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET title = ? WHERE id = ? AND user_id = ?",
        (title, task_id,user_id)
    )
    conn.commit()
    affected = cur.rowcount

    conn.close()
    return affected 



def delete_task(task_id,user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id,user_id)
    )
    conn.commit()
    affected = cur.rowcount

    conn.close()
    return affected