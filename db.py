import sqlite3

def create_books_table():
    conn = sqlite3.connect("books.sqlite")
    cursor = conn.cursor()
    sql_query = """ CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        author TEXT NOT NULL,
        language TEXT NOT NULL,
        title TEXT NOT NULL
    )"""
    cursor.execute(sql_query)
    conn.commit()
    conn.close()

create_books_table()