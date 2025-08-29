import sqlite3

# Database file
DB_FILE = 'users.db'

# Initialize the database
def init_db():
    # Connect to the SQLite database
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Create the users table with email column if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        # Commit changes and close the connection
        conn.commit()

# Initialize the database
init_db()

print("Database recreated successfully.")
