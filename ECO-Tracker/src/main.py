import flet as ft

def main(page):  # Removed type annotation for compatibility
    # ===== THEME & STYLING =====
    page.title = "🌱 Eco-Action Tracker"
    page.padding = 30
    
    # Set theme mode (works in both old and new Flet)
    if hasattr(ft, "ThemeMode"):
        page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.GREEN))

    # Custom colors
    green_gradient = ["#2ecc71", "#27ae60"]
    blue_gradient = ["#3498db", "#2980b9"]

    # ===== STATE =====
    points = 0
    max_points = 100

    # ===== UI COMPONENTS =====
    # Header with compatible icon reference
    try:
        eco_icon = ft.Icon(ft.icons.ECO, size=40, color="green")
    except:
        eco_icon = ft.Icon(name="eco", size=40, color="green")

    header = ft.Row(
        controls=[
            eco_icon,
            ft.Text("ECO TRACKER", size=28, weight="bold"),
            ft.IconButton(
                icon=ft.icons.DARK_MODE if hasattr(ft, "icons") else "dark_mode",
                on_click=lambda e: toggle_theme(),
                tooltip="Toggle theme"
            )
        ],
        alignment="spaceBetween"
    )

    # Points Display
    points_display = ft.Column([
        ft.Text(f"🌿 {points} POINTS", size=24, weight="bold"),
        ft.ProgressBar(
            value=points/max_points,
            color="green",
            bgcolor="#e0e0e0",
            height=10,
            width=300
        )
    ], spacing=5)

    # Action Cards
    action_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.icons.ADD_CIRCLE_OUTLINE if hasattr(ft, "icons") else "add_circle_outline", color="green"),
                    title=ft.Text("Log Eco Action", weight="bold"),
                ),
                ft.ElevatedButton(
                    "➕ Add Action",
                    on_click=log_action,
                    color="white",
                    bgcolor=green_gradient[0] if not hasattr(ft, "LinearGradient") else green_gradient,
                    style=ft.ButtonStyle(
                        shape={"": ft.RoundedRectangleBorder(radius=10)},
                        padding=20
                    )
                )
            ], spacing=10),
            padding=20,
            border_radius=10
        ),
        elevation=5
    )

    # ===== FUNCTIONS =====
    def log_action(e):
        nonlocal points
        points += 10
        update_ui()
        show_snackbar("✅ +10 Points! Keep it up!")

    def toggle_theme():
        if hasattr(ft, "ThemeMode"):
            page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        else:
            # Fallback for older versions
            page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=ft.colors.BLUE if page.theme.color_scheme.primary == ft.colors.GREEN else ft.colors.GREEN
                )
            )
        page.update()

    def update_ui():
        points_display.controls[0].value = f"🌿 {points} POINTS"
        points_display.controls[1].value = points/max_points
        page.update()

    def show_snackbar(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            action="OK",
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    # ===== FINAL LAYOUT =====
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Divider(height=20, color="transparent"),
                points_display,
                ft.Divider(height=30, color="transparent"),
                action_card,
            ],
            spacing=0,
            horizontal_alignment="center"
        )
    )

# Run the app
ft.app(target=main)