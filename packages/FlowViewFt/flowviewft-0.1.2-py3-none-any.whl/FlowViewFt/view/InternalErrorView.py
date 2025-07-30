from ..core.FlowViewFtView import FlowViewFtView
import flet as ft


class InternalErrorView(FlowViewFtView):
    def build(self):
        return ft.View(
            route="/500",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.AppBar(
                    title=ft.Text("Internal Error", size=22, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    center_title=True,
                    elevation=2,
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=30, vertical=40),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.Icon(
                                name=ft.Icons.REPORT_PROBLEM_ROUNDED,
                                size=90,
                                color=ft.Colors.RED_600
                            ),
                            ft.Text(
                                "¡Ups! Something has gone wrong..",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "An unexpected error has occurred in the application.",
                                size=16,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(
                                visible=self.debug,
                                padding=ft.padding.all(16),
                                bgcolor=ft.Colors.RED_50,
                                border=ft.border.all(1, ft.Colors.RED_200),
                                border_radius=8,
                                content=ft.Text(
                                    self.error if hasattr(self, "error") and self.error else "Unknown error",
                                    size=13,
                                    selectable=True,
                                    color=ft.Colors.RED_800
                                ),
                            ),
                            ft.ElevatedButton(
                                "Back to top",
                                on_click=lambda _: self.page.go("/"),
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                width=200,
                            ),

                        ]
                    )
                )
            ]
        )
    