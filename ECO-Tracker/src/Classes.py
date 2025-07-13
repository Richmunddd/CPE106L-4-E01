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
        """Logs an eco action and adds points to the user's account."""
        self.eco_points += points
        self.save()

    def earn_points(self, points):
        """Add points to the user's eco_points."""
        self.eco_points += points
        self.save()

    def spend_points(self, points):
        """Spend points from the user's account."""
        if self.eco_points >= points:
            self.eco_points -= points
            self.save()
        else:
            raise ValueError("Not enough points to spend.")

    def set_password(self, plain_text_password):
        """Hash and set the user's password."""
        self.password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, plain_text_password):
        """Check if the given password matches the stored hashed password."""
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), self.password.encode('utf-8'))

    def join_challenge(self, challenge):
        """Add this user to a challenge."""
        CommunityChallenge.add_participant(self, challenge)

    def view_leaderboard(self):
        """Fetch the leaderboard of eco actions."""
        leaderboard = EnvironmentalDataAPI.fetch_leaderboard_data()
        return leaderboard

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, eco_points={self.eco_points})"


class EcoPointSystem:
    """Handles eco points and related transactions."""
    transaction_history = []

    @staticmethod
    def track_transaction(user_id, points):
        """Track eco points transactions."""
        EcoPointSystem.transaction_history.append({"user_id": user_id, "points": points})
        EcoPointSystem.apply_point_conversion_rate(user_id, points)

    @staticmethod
    def apply_point_conversion_rate(user_id, points):
        """Apply point conversion logic (e.g., multiplying with a conversion rate)."""
        conversion_rate = 1.0  # Define point conversion rate here
        adjusted_points = points * conversion_rate
        # You could adjust the user's points here if needed.


class CarbonFootprintAPI:
    """Calculates the carbon footprint of actions."""
    @staticmethod
    def calculate_footprint(action_name):
        """Calculates the carbon impact of a specific action."""
        action_impact = {
            "recycle": 0.5,  # Example: 0.5 kg CO2 per recycle action
        }
        return action_impact.get(action_name.lower(), 0)


class EnvironmentalDataAPI:
    """Fetches dynamic leaderboard and environmental data."""
    @staticmethod
    def fetch_leaderboard_data():
        """Fetch the leaderboard data (example data below)."""
        return [
            {"name": "User1", "eco_points": 100},
            {"name": "User2", "eco_points": 80},
        ]


class CommunityChallenge:
    """Handles community challenges."""
    challenges = []

    @staticmethod
    def create_challenge(challenge_details):
        """Create a new challenge."""
        challenge = {
            "challenge_name": challenge_details['name'],
            "goal": challenge_details['goal'],
            "reward_points": challenge_details['reward_points'],
            "participants": []
        }
        CommunityChallenge.challenges.append(challenge)

    @staticmethod
    def add_participant(user, challenge):
        """Add a user to a challenge."""
        challenge['participants'].append(user)
        print(f"{user.name} joined the challenge: {challenge['challenge_name']}")

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

