import sqlite3
import bcrypt

class User:
    def __init__(self, name, user_id=None, password=None):
        self.id = user_id
        self.name = name
        self.eco_points = 0
        self.password = password  # Store password in the object
        if user_id:
            self.load(user_id)

    def load(self, user_id):
        conn = sqlite3.connect("eco_actions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, eco_points, password FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            self.id, self.name, self.eco_points, self.password = user_data
        conn.close()

    def save(self):
        conn = sqlite3.connect("eco_actions.db")
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE users SET name = ?, eco_points = ?, password = ? WHERE id = ?", 
                           (self.name, self.eco_points, self.password, self.id))
        else:
            cursor.execute("INSERT INTO users (name, eco_points, password) VALUES (?, ?, ?)", 
                           (self.name, self.eco_points, self.password))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def log_action(self, action_name, points):
        self.eco_points += points
        self.save()

    def set_password(self, plain_text_password):
        """Hash and set the user's password."""
        self.password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, plain_text_password):
        """Check if the given password matches the stored hashed password."""
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), self.password.encode('utf-8'))

# Function to initialize the database
def init_db():
    conn = sqlite3.connect("eco_actions.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            eco_points INTEGER DEFAULT 0,
            password TEXT NOT NULL  -- Add the password field
        )
    ''')
    conn.commit()
    conn.close()

