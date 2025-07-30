import flet as ft
from FlowViewFt import FlowViewFtView
from state.counter_state import counter_state

class CounterView(FlowViewFtView):
    def __init__(self, page):
        super().__init__(page)
        self.state = counter_state(self.page)
    def build(self):
        return ft.View(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.REMOVE, 
                            on_click=self.state.minus_click
                        ),
                        self.state.txt_number,
                        ft.IconButton(
                            ft.Icons.ADD, 
                            on_click=self.state.plus_click
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.ElevatedButton(
                    "Go to Home",
                    on_click=lambda _: self.pop_go("/"),
                ),
            ]
        )
