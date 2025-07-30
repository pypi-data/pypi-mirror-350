import re
import flet as ft
from urllib.parse import urlparse, parse_qs
import inspect

class Router:
    def __init__(self):
        self.routes = {}
        self.protected_routes = set()
        self.page = None
        self.current_route = "/"
        self.is_authenticated = False
        self.history = []  # Track navigation history

    def route(self, path, protected=False):
        def decorator(func):
            self.routes[path] = func
            if protected:
                self.protected_routes.add(path)
            return func
        return decorator

    def attach(self, page: ft.Page):
        self.page = page
        page.on_route_change = self._on_route_change
        page.on_view_pop = self._on_view_pop
        if self.page.route:
            self.history = [self.page.route]  # Initialize history with initial route
            self._render_route(self.page.route)

    def login(self):
        self.is_authenticated = True
        self.page.client_storage.set("is_authenticated", "true")
        print(self.page.client_storage.get("is_authenticated"))
        self.go("/")

    def logout(self):
        self.is_authenticated = False
        self.page.client_storage.remove("is_authenticated")
        self.go("/")

    def go(self, route: str):
        self.current_route = route
        # Update history: remove current route if present, append new route
        if self.history and self.history[-1] == route:
            return  # Avoid duplicate consecutive routes
        self.history.append(route)
        self.page.go(route)

    def pop(self):
        if len(self.history) > 1:
            self.history.pop()  # Remove current route
            previous_route = self.history[-1]  # Get previous route
            self.current_route = previous_route
            self.page.go(previous_route)
        else:
            self.current_route = "/"
            self.page.go("/")  # Fallback to "/" if no history

    def _on_view_pop(self, e: ft.ViewPopEvent):
        self.pop()

    def _on_route_change(self, e: ft.RouteChangeEvent):
        print(self.page.route)
        self._render_route(e.route)

    def _render_route(self, full_route):
        parsed = urlparse(full_route)
        path = parsed.path
        query_params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        self.current_route = full_route

        # Update history: ensure current route is at the end
        if self.history and self.history[-1] != full_route:
            self.history.append(full_route)
        elif not self.history:
            self.history.append(full_route)

        matched_route, path_params = self._match_route(path)

        if not matched_route:
            # Append 404 view instead of clearing stack
            self.page.views.append(
                ft.View(
                    route=full_route,
                    controls=[
                        ft.AppBar(
                            leading=ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                icon_color="black",
                                on_click=lambda _: self.pop()
                            )
                        ),
                        ft.Text("404", color="black", size=80, weight="bold", text_align="center"),
                        ft.Text("Page Not Found", color="black", size=26, text_align="center"),
                    ],
                    spacing=0,
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=10
                )
            )
            self.page.update()
            return

        if matched_route in self.protected_routes and not self.is_authenticated:
            self.page.go(f"/login?next={full_route}")
            return

        if matched_route:
            view_func = self.routes[matched_route]
            all_params = {**path_params, **query_params}

            sig = inspect.signature(view_func)
            valid_params = {
                name: value
                for name, value in all_params.items()
                if name in sig.parameters and name != 'page'
            }

            content = view_func(self.page, **valid_params)

            if not self.page.views or self.page.views[-1].route != full_route:
                self.page.views.clear()
                if isinstance(content, ft.View):
                    self.page.views.append(content)
                else:
                    self.page.views.append(ft.View(route=full_route, controls=[content]))

        self.page.update()

    def _match_route(self, path: str):
        for route_pattern, handler in self.routes.items():
            param_names = re.findall(r":(\w+)", route_pattern)
            regex_pattern = re.sub(r":\w+", r"([^/]+)", route_pattern)
            match = re.match(f"^{regex_pattern}$", path)
            if match:
                values = match.groups()
                params = dict(zip(param_names, values))
                return route_pattern, params
        return None, {}