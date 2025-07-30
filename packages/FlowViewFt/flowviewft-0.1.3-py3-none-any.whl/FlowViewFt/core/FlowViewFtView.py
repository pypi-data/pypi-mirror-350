from flet import Page, View
from .FlowViewFtState import FlowViewFtState
from .FlowViewFtParams import FlowViewFtParams
from typing import Optional
import asyncio

class FlowViewFtView:
    def __init__(
            self, 
            page: Page, 
            state: Optional[FlowViewFtState] = None, 
            params: Optional[FlowViewFtParams] = None
        ):
        self.page = page
        self.state = state
        self.params = params
        self.debug = False
        self.error = ""

    def get_param(self, var: str):
        if self.params is None:
            return None
        return self.params.get(var)

    def get_all_param(self):
        if self.params is None:
            return None
        return self.params.get_all()

    def update(self):
        self.page.update()

    async def update_async(self):
        await asyncio.sleep(0)
        self.page.update()

    def go(self, route):
        self.page.go(route=route)

    def pop_go(self, route):
        if len(self.page.views) >= 1:
            self.page.views.pop()
            self.page.go(route=route)

    def pop_all_go(self, route):
        self.page.views.clear()
        self.page.go(route=route)

    

    def build(self) -> View:
        raise NotImplementedError("You must implement the build() method.")

    def onBuildComplete(self):
        ...