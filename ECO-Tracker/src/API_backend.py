from fastapi import FastAPI, HTTPException
import sqlite3
from Classes import User, init_db
from pydantic import BaseModel
import uvicorn
import bcrypt
from fastapi.responses import JSONResponse
from multiprocessing import Process
import flet as ft
from flet_app import main

app = FastAPI()

# Initialize the database
init_db()

# Pydantic models for request and response
class UserRequest(BaseModel):
    name: str
    password: str  # Including password as part of the request body

class ActionRequest(BaseModel):
    user_id: int
    action_name: str
    points: int

@app.post("/create_user/")
def create_user(user_request: UserRequest):
    # Hash the password before saving
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())
    user = User(user_request.name, password=hashed_password)
    user.save()
    return {"user_id": user.id, "name": user.name}

@app.post("/log_action/")
def log_action(action_request: ActionRequest):
    user = User(action_request.user_id)
    user.log_action(action_request.action_name, action_request.points)
    return {"message": f"Action {action_request.action_name} logged for {user.name}."}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    conn = sqlite3.connect("eco_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, eco_points FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return {"name": user_data[0], "eco_points": user_data[1]}
    else:
        return {"error": "User not found"}

@app.get("/leaderboard/")
def leaderboard():
    conn = sqlite3.connect("eco_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, eco_points FROM users ORDER BY eco_points DESC")
    leaderboard_data = cursor.fetchall()
    conn.close()
    return [{"name": user[0], "eco_points": user[1]} for user in leaderboard_data]

@app.post("/sign_up/")
def sign_up(user_request: UserRequest):
    # Hash the password before saving
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())
    user = User(user_request.name, password=hashed_password)
    user.save()
    return {"user_id": user.id, "name": user.name}

@app.post("/login/")
def login(user_request: UserRequest, password: str):
    conn = sqlite3.connect("eco_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, password FROM users WHERE name = ?", (user_request.name,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_id, name, stored_hash = user_data
        # Compare the password with the stored hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):  # Ensure both are bytes
            return {"user_id": user_id, "name": name}
        else:
            raise HTTPException(status_code=400, detail="Invalid password")
    else:
        raise HTTPException(status_code=400, detail="User not found")
    
if __name__ == "__main__":
    # Start the FastAPI app in a separate process
    fastapi_process = Process(target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000))
    fastapi_process.start()

    # Start the Flet UI app in another process
    flet_process = Process(target=ft.app, args=(main,))
    flet_process.start()

    # Join processes to keep them running
    fastapi_process.join()
    flet_process.join()
