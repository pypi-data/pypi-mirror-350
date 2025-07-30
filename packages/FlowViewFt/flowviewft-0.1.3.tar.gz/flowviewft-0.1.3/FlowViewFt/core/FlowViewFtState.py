from flet import Page
from typing import Callable
import asyncio

class FlowViewFtState:
    def __init__(self, page: Page):
        self.page = page

    def update(self):
        self.page.update()

    async def update_async(self):
        await asyncio.sleep(0)
        self.page.update()

    def go(self, route: str):
        if route:
            self.page.go(route)

    def pop_go(self, route: str):
        if len(self.page.views) >= 1:
            self.page.views.pop()
            self.page.go(route)

    def pop_all_go(self, route: str):
        self.page.views.clear()
        self.page.go(route)

    def inject_in_state(self, func: Callable):
        setattr(self, func.__name__, func)
