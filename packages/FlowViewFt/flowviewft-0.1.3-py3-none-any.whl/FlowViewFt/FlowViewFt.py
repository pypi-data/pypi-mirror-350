from typing import Optional
from repath import match
import traceback
import flet as ft
# core
from .core.FlowViewFtView import FlowViewFtView
from .core.FlowViewFtState import FlowViewFtState
from .core.FlowViewFtParams import FlowViewFtParams
from .core.FlowViewFtMiddleware import FlowViewFtMiddleware
# view
from .view.NotFoundView import NotFoundView
from .view.InternalErrorView import InternalErrorView

def route(path: str, view: type[FlowViewFtView]) -> dict:
    return {"route": path, "view": view}

def route_str(route):
    return str(route.route) if not isinstance(route, str) else route

class FlowViewFt:
    def __init__(
        self,
        page: ft.Page,
        routes: list[dict],
        state: Optional[FlowViewFtState] = None,
        middleware_cls: Optional[type[FlowViewFtMiddleware]] = None,
        init_route: Optional[str] = None,
        not_found_view: type[FlowViewFtView] = NotFoundView,
        internal_error_view: type[FlowViewFtView] = InternalErrorView,
        debug: bool = True,
    ):
        self.__debug = debug
        self.__page = page
        self.__middleware_cls = middleware_cls
        self.__routes = routes
        self.__params = FlowViewFtParams()
        self.__not_found_view = not_found_view
        self.__internal_error_view = internal_error_view
        self.__state = state or FlowViewFtState(page)

        

        self.__page.on_route_change = self.route_event_handler
        if self.__page.views:
            self.__page.views.clear()
        self.route_event_handler(init_route or self.__page.route)

    def route_event_handler(self, route):
        try:
            route_str_value = route_str(route)

            for r in self.__routes:
                route_match = match(r["route"], route_str_value)
                if route_match:
                    self.__handle_route_match(r, route_match, route_str_value)
                    return

            self.__render_view(self.__not_found_view)

        except Exception:
            self.__render_view(self.__internal_error_view, error=traceback.format_exc(110))

    def __handle_route_match(self, route_entry, route_match, route_str_value):
        self.__params = FlowViewFtParams(route_match.groupdict())

        if self.__middleware_cls:
            middleware = self.__middleware_cls(self.__page, self.__state, self.__params)
            middleware.middleware()

        view = route_entry["view"](page=self.__page)
        self.__inject_state_and_params(view)
        self.__build_and_update_view(view)

    def __inject_state_and_params(self, view):
        if not hasattr(view, "state") or view.state is None:
            if isinstance(self.__state, FlowViewFtState):
                view.state = self.__state
        view.params = self.__params
        view.debug = self.__debug

    def __build_and_update_view(self, view):
        self.__page.views.clear()
        self.__page.views.append(view.build())
        self.__page.update()
        view.onBuildComplete()

    def __render_view(self, view_cls, error=None):
        view = view_cls(self.__page)
        self.__inject_state_and_params(view)
        if error and hasattr(view, "error"):
            view.error = error
        self.__build_and_update_view(view)
