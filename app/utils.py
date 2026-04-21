import os
import sqlite3

def get_db_connection(db_path):
    """Basic database helper."""
    return sqlite3.connect(db_path)

def query_user(conn, user_id):
    """
    Intentional weakness: SQL injection via string formatting
    Bandit will flag this as B608 (hardcoded SQL)
    """
    #hellllooo
    cursor = conn.cursor()
    # NEVER format SQL strings with user input
    query = f"SELECT * FROM users WHERE id = {user_id}"   # <-- B608: SQL injection
    cursor.execute(query)
    return cursor.fetchall()

def read_file(filename):
    """Simple file reader."""
    with open(filename, 'r') as f:
        return f.read()