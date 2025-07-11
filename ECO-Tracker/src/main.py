import flet as ft

class EcoActionApp(ft.Control):  # Ensure you're using UserControl
    def __init__(self):
        super().__init__()
        self.points = 0

    def build(self):
        # Define UI components
        self.log_action_button = ft.ElevatedButton(text="Log Eco Action", on_click=self.log_eco_action)
        self.earn_points_label = ft.Text(f'Earned Points: {self.points}')
        self.join_challenge_button = ft.ElevatedButton(text="Join Challenge", on_click=self.join_challenge)
        self.view_leaderboard_button = ft.ElevatedButton(text="View Leaderboard", on_click=self.view_leaderboard)

        # Return a Column with the controls
        return ft.Column(
            controls=[
                self.log_action_button,
                self.earn_points_label,
                self.join_challenge_button,
                self.view_leaderboard_button
            ]
        )

    def log_eco_action(self, e):
        # Simulate logging an eco-action and earning points
        self.points += 10
        self.update_points_label()

    def update_points_label(self):
        self.earn_points_label.value = f'Earned Points: {self.points}'
        self.update()

    def join_challenge(self, e):
        ft.SnackBar("You joined a challenge!", duration=2000).show()

    def view_leaderboard(self, e):
        ft.SnackBar("Displaying leaderboard...", duration=2000).show()

    def _get_control_name(self):
        return "EcoActionApp"

def main(page):
    page.title = "Eco-Action Tracker"
    app = EcoActionApp()
    page.add(app)

# Run the app in web mode
ft.app(target=main)



