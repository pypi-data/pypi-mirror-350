import flet as ft
from FlowViewFt import FlowViewFt, route
from view.home_view import HomeView
from view.counter_view import CounterView

def main(page: ft.Page):
    page.title = "Counter App"

    FlowViewFt(
        page=page,
        routes=[
            route("/", HomeView),
            route("/counter", CounterView),
        ],
        init_route="/",
    )

ft.app(target=main)
