import flet as ft

def main(page):
    # Add some text to the page
    page.add(ft.Text("Hello, Web Flet!"))

# Start the app for web browser
ft.app(target=main, view=ft.WEB_BROWSER)

