import sqlite3

def create_user_table():
    conn = sqlite3.connect("users.sqlite")
    cursor = conn.cursor()
    sql_query = """ CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )"""
    cursor.execute(sql_query)
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [
        dict(id=row[0], username=row[1], email=row[2], password=row[3])
        for row in cursor.fetchall()
    ]
    conn.close()
    return users

def add_user(username, email, password):
    conn = sqlite3.connect("users.sqlite")
    cursor = conn.cursor()
    sql_query = """INSERT INTO users (username, email, password)
                   VALUES (?, ?, ?)"""
    cursor.execute(sql_query, (username, email, password))
    conn.commit()
    conn.close()

# Create the users table if it doesn't exist
create_user_table()