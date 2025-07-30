from repath import match
import flet as ft

from .FlowViewFtState import FlowViewFtState
from .FlowViewFtParams import FlowViewFtParams

class FlowViewFtMiddleware:
    def __init__(self, page: ft.Page, state: FlowViewFtState, params: FlowViewFtParams):
        self.page = page
        self.state = state
        self._params = params
        self.init()

    def init(self)->None:
        ...

    def middleware(self)->None:
        ...

    def get_param(self, var: str):
        return self._params.get(var)
    
    def get_all_param(self)->dict:
        return self._params.get_all()
    
    def get_curunt_route(self)->str:
        return self.page.route 
    
    def redirect_route(self,route)->None:
        self.page.route = route

    def is_route_match(self, route) -> bool:
        return match(route, self.page.route) is not None

    def is_route_not_matched(self, route) -> bool:
        return match(route, self.page.route) is None