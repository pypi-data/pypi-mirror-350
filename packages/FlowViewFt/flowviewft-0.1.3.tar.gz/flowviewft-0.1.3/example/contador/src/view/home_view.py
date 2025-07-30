import flet as ft
from FlowViewFt import FlowViewFtView

class HomeView(FlowViewFtView):
    def build(self):
        return ft.View(
            controls=[
                ft.Text(
                    "Welcome to a CounterApp", 
                    size=30
                ),
                ft.ElevatedButton(
                    "Go to Counter", 
                    on_click=lambda _: self.page.go("/counter")
                ),
            ]
        )
