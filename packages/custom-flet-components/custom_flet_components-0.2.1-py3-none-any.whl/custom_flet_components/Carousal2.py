import flet as ft
import asyncio

class ScreenWidget2:
    def __init__(self, controls, bgcolor="white"):
        self.controls = controls
        self.bgcolor = bgcolor

    def build(self):
        return ft.Container(
            content=ft.Column(
                self.controls,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=self.bgcolor,
            expand=True,
            alignment=ft.alignment.center
        )

class CarouselWidget2(ft.Column):
    def __init__(self, screens, animation_type=ft.AnimatedSwitcherTransition.FADE, 
                 auto_play_interval=3, on_change=None, width=None, height=None,
                 icon_color=ft.Colors.BLUE, icon_bgcolor=ft.Colors.TRANSPARENT, icon_overlay_color=ft.Colors.TRANSPARENT):
        self.screens = screens
        self.auto_play_interval = auto_play_interval
        self.on_change = on_change
        self.current_index = 0
        self.is_auto_playing = True
        
        # Animated switcher for screen transitions
        self.switcher = ft.AnimatedSwitcher(
            content=self.screens[0].build(),
            transition=animation_type,
            duration=600,
            reverse_duration=600,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
            expand=True
        )
        
        # Back button
        self.back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_OUTLINED,
            icon_color=icon_color,
            on_click=self.back,
            style=ft.ButtonStyle(
                bgcolor=icon_bgcolor,
                overlay_color=icon_overlay_color
            )
        )
        
        # Next button
        self.next_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_OUTLINED,
            rotate=3,
            icon_color=icon_color,
            on_click=self.next,
            style=ft.ButtonStyle(
                bgcolor=icon_bgcolor,
                overlay_color=icon_overlay_color
            )
        )

        # Initialize Column with width and height
        super().__init__(
            controls=[
                ft.Container(
                    content=ft.Row(
                        [
                            self.back_button,
                            self.switcher,
                            self.next_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=0
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                    margin=0
                )
            ],
            width=width,
            height=height,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def update_progress_bars(self):
        for i, progress_bar in enumerate(getattr(self, "progress_bars", [])):
            progress_bar.value = 1.0 if i == self.current_index else 0.0
            progress_bar.update()

    def did_mount(self):
        if self.auto_play_interval > 0:
            self.page.run_task(self.auto_play)

    async def auto_play(self):
        while self.is_auto_playing and len(self.screens) > 1:
            await asyncio.sleep(self.auto_play_interval)
            if self.is_auto_playing:
                self.current_index = (self.current_index + 1) % len(self.screens)
                self.switcher.content = self.screens[self.current_index].build()
                self.switcher.update()
                self.update_progress_bars()
                if self.on_change:
                    self.on_change(self.current_index)

    def next(self, e):
        self.is_auto_playing = False
        self.current_index = (self.current_index + 1) % len(self.screens)
        self.switcher.content = self.screens[self.current_index].build()
        self.switcher.update()
        self.update_progress_bars()
        if self.on_change:
            self.on_change(self.current_index)
        self.page.run_task(self.resume_auto_play)

    def back(self, e):
        self.is_auto_playing = False
        self.current_index = (self.current_index - 1) % len(self.screens)
        self.switcher.content = self.screens[self.current_index].build()
        self.switcher.update()
        self.update_progress_bars()
        if self.on_change:
            self.on_change(self.current_index)
        self.page.run_task(self.resume_auto_play)

    async def resume_auto_play(self):
        await asyncio.sleep(2)
        self.is_auto_playing = True

    def will_unmount(self):
        self.is_auto_playing = False

# def main(page: ft.Page):
#     page.title = "Carousel Demo"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.window.always_on_top = True
#     page.theme_mode = "light"
#     page.padding = 0

#     screens = [
#         ScreenWidget2(
#             controls=[
#                 ft.Text("Welcome to the Carousel!", size=20),
#                 ft.Text("First screen", size=16),
#             ],
#             bgcolor="white"
#         ),
#         ScreenWidget2(
#             controls=[
#                 ft.Text("Explore Features", size=20),
#                 ft.Text("Second screen", size=16),
#             ],
#             bgcolor="white"
#         ),
#         ScreenWidget2(
#             controls=[
#                 ft.Text("Get Started", size=20),
#                 ft.Text("Third screen", size=16),
#             ],
#             bgcolor="white"
#         )
#     ]

#     carousel = CarouselWidget2(
#         screens=screens,
#         animation_type=ft.AnimatedSwitcherTransition.FADE,
#         auto_play_interval=3,
#         on_change=lambda index: print(f"Current screen: {index}"),
#         width=400,
#         height=300,
#         icon_color="white",
#         icon_bgcolor="blue",
#         icon_overlay_color="red"
#     )

#     page.add(carousel)

# ft.app(target=main)
