import flet as ft

class MyApp(ft.UserControl):
    def build(self):
        return ft.Text("Hello, Flet!")

ft.app(target=MyApp)
