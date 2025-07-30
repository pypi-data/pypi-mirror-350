from ..core.FlowViewFtView import FlowViewFtView
import flet as ft


class NotFoundView(FlowViewFtView):
    def build(self):
        ruta = self.page.route  

        return ft.View(
            route="/404",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.AppBar(
                    title=ft.Text("Page not found", size=24, weight=ft.FontWeight.BOLD),
                    bgcolor="#3F51B5", 
                    color="white",
                    center_title=True,
                    elevation=4,
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(40),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.Container(
                                content=ft.Stack(
                                    controls=[
                                        ft.Text(
                                            "404",
                                            size=120,
                                            weight=ft.FontWeight.BOLD,
                                            color="#E8EAF6",  
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Icon(
                                            name=ft.Icons.SEARCH_OFF_ROUNDED,
                                            size=70,
                                            color="#3F51B5",
                                        ),
                                    ]
                                ),
                                alignment=ft.alignment.center,
                                height=140,
                            ),
                            ft.Text(
                                "Oops! Page not found",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"The route '{ruta}' does not exist or has been moved.",
                                    size=16,
                                    color="#757575",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=400,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "Check the URL or use the navigation to find what you are looking for.",
                                    size=16,
                                    color="#757575",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=500,
                            ),
                            ft.Container(height=20), 
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=15,
                                controls=[
                                    ft.ElevatedButton(
                                        "Go to start",
                                        icon=ft.Icons.HOME,
                                        on_click=lambda _: self.page.go("/"),
                                        style=ft.ButtonStyle(
                                            color="white",
                                            bgcolor="#3F51B5", 
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )