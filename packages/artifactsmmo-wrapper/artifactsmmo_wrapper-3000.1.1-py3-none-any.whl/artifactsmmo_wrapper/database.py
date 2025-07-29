import sqlite3
import os

# --- Ensure 'db' Directory Exists ---
db_dir = 'db'
db_file = os.path.join(db_dir, 'artifacts.db')

if not os.path.exists(db_dir):
    os.makedirs(db_dir)  # Create the 'db' directory if it doesn't exist

# --- Database Loading ---
if not os.path.exists(db_file):
    with open(db_file, 'w', encoding='utf-8') as f:
        f.truncate(0)  # Ensure the file is created empty

cache_db = sqlite3.connect(db_file)
cache_db.row_factory = sqlite3.Row
cache_db_cursor = cache_db.cursor()
cache_db_cursor.execute("CREATE TABLE IF NOT EXISTS cache_table (k TEXT PRIMARY KEY, v TEXT)")
cache_db.commit()

# Export the database connection and cursor
__all__ = ['cache_db', 'cache_db_cursor']
