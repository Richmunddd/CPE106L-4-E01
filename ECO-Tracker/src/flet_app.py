import flet as ft
import requests
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import multiprocessing  # Use multiprocessing instead of threading
import json

API_URL = "http://127.0.0.1:8000"

# Function to handle the Sign Up UI
def sign_up_ui(page: ft.Page):
    page.title = "Sign Up"
    page.bgcolor = "#1D1F27"  # Bluish-Black background

    # Clear any existing UI elements on the page
    page.controls.clear()

    # Title and message
    page.add(
        ft.Text("Sign Up", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
        ft.Text("Create a new account to start using Eco Action Tracker.", size=16, color=ft.Colors.GREEN_600),
        ft.Divider(color=ft.Colors.GREEN_400),  # Decorative divider
    )

    # Input fields for name and password
    name_field = ft.TextField(label="Enter your name", border_color=ft.Colors.GREEN_400, autofocus=True)
    password_field = ft.TextField(label="Enter your password", password=True, border_color=ft.Colors.GREEN_400)

    # Snack bar for messages
    snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.GREEN_200)

    # Sign-Up function
    def sign_up(e):
        name = name_field.value
        password = password_field.value
        
        if not name or not password:
            snack_bar.content = ft.Text("Please enter both name and password.", color=ft.Colors.RED_700)
            snack_bar.open = True
            page.snack_bar = snack_bar
            page.update()
            return
        
        # Make POST request to backend for creating user
        response = requests.post(f"{API_URL}/sign_up/", json={"name": name, "password": password})
        
        if response.status_code == 200:
            snack_bar.content = ft.Text("User created successfully!", color=ft.Colors.GREEN_700)
            snack_bar.open = True
            page.snack_bar = snack_bar
            page.update()

            # After successful sign up, show the login UI
            page.controls.clear()
            login_ui(page)
        else:
            snack_bar.content = ft.Text("Failed to create user.", color=ft.Colors.RED_700)
            snack_bar.open = True
            page.snack_bar = snack_bar
            page.update()

    # Add controls to the page inside a container with a rounded square shape
    page.add(
        ft.Container(
            ft.Column(
                [
                    name_field,
                    password_field,
                    ft.ElevatedButton("Sign Up", on_click=sign_up, bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Already have an account? Login", on_click=lambda e: login_ui(page), bgcolor=ft.Colors.GREY_300, color=ft.Colors.BLACK),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            margin=60,  # Increased margin to create more space around the container
            width=500,  # Increased width for a larger container
            height=400,  # Increased height for a larger container
            border_radius=30,  # Rounded square edges
            bgcolor="#2C3E50",  # Dark gray background for the container, matching the theme
            padding=30,  # Padding added to create space around the input fields
        ),
    )

# Function to handle the Login UI
def login_ui(page: ft.Page):
    page.title = "Login"
    page.bgcolor = "#1D1F27"  # Bluish-Black background

    # Clear any existing UI elements on the page
    page.controls.clear()

    # Title and message
    page.add(
        ft.Text("Login", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
        ft.Text("Welcome back! Please log in to your account.", size=25, color=ft.Colors.GREEN_600),
        ft.Divider(color=ft.Colors.GREEN_400),  # Decorative divider
    )

    # Input fields for name and password
    name_field = ft.TextField(label="Enter your name", border_color=ft.Colors.GREEN_400)
    password_field = ft.TextField(label="Enter your password", password=True, border_color=ft.Colors.GREEN_400)

    # Snack bar for messages
    snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.GREEN_200)

    # Login function
    def login(e):
        name = name_field.value
        password = password_field.value
        
        # Make POST request to backend for logging in
        response = requests.post(f"{API_URL}/login/", json={"name": name, "password": password})
        
        if response.status_code == 200:
            snack_bar.content = ft.Text("Login successful!", color=ft.Colors.GREEN_700)
            snack_bar.open = True
            page.snack_bar = snack_bar
            page.update()

            # Here you can navigate to the main content like challenges, leaderboard, etc.
            page.controls.clear()
            page.add(
                ft.Text("Welcome to the Eco Action Tracker!", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                ft.Text("You are logged in!", size=25, color=ft.Colors.GREEN_600),
            )
            page.update()

        else:
            snack_bar.content = ft.Text("Failed to login. Please check your credentials.", color=ft.Colors.RED_700)
            snack_bar.open = True
            page.snack_bar = snack_bar
            page.update()

    # Add controls to the page inside a container with a rounded square shape
    page.add(
        ft.Container(
            ft.Column(
                [
                    name_field,
                    password_field,
                    ft.ElevatedButton("Login", on_click=login, bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Don't have an account? Sign Up", on_click=lambda e: sign_up_ui(page), bgcolor=ft.Colors.GREY_300, color=ft.Colors.BLACK),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            margin=60,  # Increased margin to create more space around the container
            width=500,  # Increased width for a larger container
            height=400,  # Increased height for a larger container
            border_radius=30,  # Rounded square edges
            bgcolor="#2C3E50",  # Dark gray background for the container, matching the theme
            padding=30,  # Padding added to create space around the input fields
        ),
    )


def main(page: ft.Page):
    page.title = "Eco Action Tracker"
    page.bgcolor = "#1D1F27"  # Bluish-Black background

    # Initially, show the login UI
    login_ui(page)


def start_flet_app():
    ft.app(target=main)


if __name__ == "__main__":
    # Use multiprocessing to run Flet app and FastAPI server in separate processes
    flet_process = multiprocessing.Process(target=start_flet_app)
    flet_process.start()
    flet_process.join()


