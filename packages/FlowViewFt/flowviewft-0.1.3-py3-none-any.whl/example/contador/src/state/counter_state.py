from FlowViewFt import FlowViewFtState
import flet as ft
class counter_state(FlowViewFtState):
    def __init__(self, page):
        super().__init__(page)
        self.txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(self,e):
        if self.txt_number.value is not None:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
        self.update()

    def plus_click(self,e):
        if self.txt_number.value is not None:
            self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()
