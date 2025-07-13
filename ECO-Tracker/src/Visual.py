import matplotlib.pyplot as plt
import io
import base64
import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"

def fetch_leaderboard():
    """Fetch leaderboard data from API."""
    response = requests.get(f"{API_URL}/leaderboard/")
    if response.status_code == 200:
        return response.json()
    return []

def create_leaderboard_graph():
    """Generate a graph of the leaderboard."""
    leaderboard_data = fetch_leaderboard()

    if not leaderboard_data:
        return None

    names = [user['name'] for user in leaderboard_data]
    points = [user['eco_points'] for user in leaderboard_data]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(names, points, color='green')
    plt.xlabel('Eco Points')
    plt.title('Leaderboard - Eco Points')
    
    # Save the plot to a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_data = buf.read()
    encoded_img = base64.b64encode(img_data).decode('utf-8')
    
    return f"data:image/png;base64,{encoded_img}"

def main(page: ft.Page):
    page.title = "Eco Action Tracker"
    
    # Create and display leaderboard graph
    graph_image = create_leaderboard_graph()
    
    if graph_image:
        page.add(ft.Image(src=graph_image))
    else:
        page.add(ft.Text("Failed to load leaderboard data"))

# Run the app
ft.app(target=main)
