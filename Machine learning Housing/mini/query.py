import sqlite3

# Database file
DB_FILE = 'users.db'

# Query the database for user details
def get_user(username):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        print(user)  # This will print the user details

# Example usage
get_user('Ravikant')
