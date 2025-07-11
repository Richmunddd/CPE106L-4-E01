import flet as ft

# Create the MyApp class using Control instead of UserControl
class MyApp(ft.Control):
    def build(self):
        return ft.Text("Hello, Flet!")

# Run the app
ft.app(target=MyApp)

