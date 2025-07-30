import flet as ft
import asyncio
from flet_shimmer import Shimmer, ShimmerDirection


class UniversalShimmer:
    def __init__(
        self,
        base_color=ft.Colors.with_opacity(0.1, ft.Colors.ON_PRIMARY_CONTAINER),
        highlight_color=ft.Colors.with_opacity(0.3, ft.Colors.ON_PRIMARY_CONTAINER),
        direction=ShimmerDirection.LEFT_TO_RIGHT,
        inclination=0.0,
        enabled=True,
        loop=0,
        opacity=1.0,
        tooltip=None,
        visible=True,
        data=None,
        left=None,
        top=None,
        right=None,
        bottom=None,
    ):
        self.shimmer_props = {
            "base_color": base_color,
            "highlight_color": highlight_color,
            "direction": direction,
            "inclination": inclination,
            "enabled": enabled,
            "loop": loop,
            "opacity": opacity,
            "tooltip": tooltip,
            "visible": visible,
            "data": data,
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
        }

    def shimmer_wrap(self, content):
        return Shimmer(content=content, **self.shimmer_props)

    def create_dummy(self, target=None):
        opacity = 0.1
        color = ft.Colors.ON_PRIMARY_CONTAINER

        circle = lambda size=60: ft.Container(
            height=size,
            width=size,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=size,
        )
        rectangle = lambda height, width=None: ft.Container(
            height=height,
            width=width or height * 2.5,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=12,
        )
        tube = lambda width: ft.Container(
            height=12,
            width=width,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=20,
        )

        if target is None:
            return self.shimmer_wrap(ft.Container())

        ctrl_name = target._get_control_name()
        dummy = ft.Container()

        if ctrl_name == "text" and getattr(target, "data", None) == "shimmer_load":
            dummy = tube(len(target.value) * 7.5 if target.value else 80)

        elif ctrl_name in ["textbutton", "elevatedbutton", "outlinedbutton"] and getattr(target, "data", None) == "shimmer_load":
            dummy = rectangle(40, 120)

        elif ctrl_name == "textfield":
            dummy = rectangle(40, 300)

        elif ctrl_name == "icon" and getattr(target, "data", None) == "shimmer_load":
            dummy = circle(30)

        elif ctrl_name == "image":
            dummy = ft.Container(bgcolor=ft.Colors.with_opacity(opacity, color), width=target.width, height=target.height)

        elif ctrl_name == "circleavatar":
            dummy = circle(target.radius * 2 if getattr(target, "radius", None) else 60)

        elif ctrl_name == "row":
            dummy = ft.Row([self.create_dummy(c) for c in target.controls])

        elif ctrl_name == "column":
            dummy = ft.Column([self.create_dummy(c) for c in target.controls])

        else:
            dummy = ft.Container(
                bgcolor=ft.Colors.with_opacity(opacity, color),
                width=200,
                height=40,
                border_radius=8,
            )

        return self.shimmer_wrap(dummy)


def ShimmerWidget(
    page: ft.Page,
    controls: list,
    duration: float = 3.0,
    *,
    base_color=ft.Colors.with_opacity(0.1, ft.Colors.ON_PRIMARY_CONTAINER),
    highlight_color=ft.Colors.with_opacity(0.3, ft.Colors.ON_PRIMARY_CONTAINER),
    direction=ShimmerDirection.LEFT_TO_RIGHT,
    inclination=0.0,
    enabled=True,
    loop=0,
    opacity=1.0,
    tooltip=None,
    visible=True,
    data=None,
    left=None,
    top=None,
    right=None,
    bottom=None,
) -> ft.Container:
    # Pass all shimmer-related properties from parameters to UniversalShimmer
    shimmer_util = UniversalShimmer(
        base_color=base_color,
        highlight_color=highlight_color,
        direction=direction,
        inclination=inclination,
        enabled=enabled,
        loop=loop,
        opacity=opacity,
        tooltip=tooltip,
        visible=visible,
        data=data,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )

    placeholders = [shimmer_util.create_dummy(ctrl) for ctrl in controls]

    container = ft.Container(
        content=ft.Column(controls=placeholders, spacing=20),
        alignment=ft.alignment.center,
        padding=20,
    )

    async def replace_with_real():
        await asyncio.sleep(duration)
        container.content = ft.Column(controls=controls, spacing=20)
        page.update()

    page.run_task(replace_with_real)
    return container


# def main(page: ft.Page):
#     page.title = "Advanced Shimmer Example"
#     page.theme_mode = ft.ThemeMode.DARK
#     page.scroll = True

#     # Real content
#     controls = [
#         ft.Image(src="https://cdn.pixabay.com/photo/2025/05/07/18/46/lake-9585821_1280.jpg", width=250, height=150),
#         ft.Text("Welcome to FlexWave!", size=24, weight=ft.FontWeight.BOLD, data="shimmer_load"),
#         ft.Row([
#             ft.ElevatedButton("Get Started", data="shimmer_load"),
#             ft.OutlinedButton("Learn More", data="shimmer_load"),
#         ]),
#         ft.TextField(label="Email", data="shimmer_load"),
#         ft.Image(
#             src="https://cdn.pixabay.com/photo/2021/10/07/00/48/boat-6686952_1280.jpg",
#             width=250,
#             height=150,
#         ),
#         ft.CircleAvatar(
#             content=ft.Icon(name=ft.Icons.PERSON),
#             radius=30
#         )
#     ]

#     # Example: override shimmer colors and direction here
#     shimmer_box = ShimmerWidget(
#         page,
#         controls=controls,
#         duration=3,
#         base_color=ft.Colors.random(),
#         highlight_color=ft.Colors.random(),
#         direction=ShimmerDirection.RIGHT_TO_LEFT,
#         inclination=0.2,
#         opacity=0.8,
#         tooltip="Loading your content...",
#         loop=0,
#     )
#     page.add(shimmer_box)


# ft.app(target=main)
