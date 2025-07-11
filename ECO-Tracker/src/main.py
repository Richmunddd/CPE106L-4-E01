import flet as ft

def main(page):
    page.title = "Eco-Action Tracker"
    page.padding = 30
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    points = 0

    # UI Components
    header = ft.Text("🌿 Eco-Action Tracker", size=24, weight="bold")
    points_text = ft.Text(f"Points: {points}", size=20)

    log_button = ft.ElevatedButton(
        "Log Action (+10 pts)",
        on_click=lambda e: add_points(e),
        bgcolor="green",
        color="white"
    )

    challenge_button = ft.ElevatedButton(
        "Join Challenge",
        on_click=lambda e: show_message(page, "Challenge joined!"),
        bgcolor="blue",
        color="white"
    )

    leaderboard_button = ft.ElevatedButton(
        "View Leaderboard",
        on_click=lambda e: show_message(page, "Leaderboard coming soon!"),
        bgcolor="purple",
        color="white"
    )

    # Functions
    def add_points(e):
        nonlocal points
        points += 10
        points_text.value = f"Points: {points}"
        page.update()
        show_message(page, "+10 points! 🌟")

    def show_message(page, text):
        page.snack_bar = ft.SnackBar(ft.Text(text))
        page.snack_bar.open = True
        page.update()

    # Layout
    page.add(
        ft.Column(
            [
                header,
                ft.Divider(height=20),
                points_text,
                ft.Divider(height=20),
                log_button,
                challenge_button,
                leaderboard_button,
            ],
            spacing=20,
            alignment="center"
        )
    )

ft.app(target=main)