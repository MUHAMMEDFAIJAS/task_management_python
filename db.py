import sqlite3

Database ="task_manager.db"

def connect():
    return sqlite3.connect(Database)