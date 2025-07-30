import flet as ft
import asyncio

class Image_Box:
    def __init__(self, image: ft.Image):
        if not isinstance(image, ft.Image):
            raise ValueError("Image_Box only accepts an ft.Image instance.")
        self.image = image

    def build(self):
        return ft.Container(content=self.image, expand=True)

class ScreenWidget:
    def __init__(self, image_box: Image_Box, bgcolor="white"):
        if not isinstance(image_box, Image_Box):
            raise ValueError("ScreenWidget only accepts an Image_Box instance.")
        self.image_box = image_box
        self.bgcolor = bgcolor

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.image_box.build()
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                expand=True
            ),
            bgcolor=self.bgcolor,
            expand=True,
            alignment=ft.alignment.center
        )


class CarouselWidget(ft.Column):
    def __init__(self, screens, animation_type=ft.AnimatedSwitcherTransition.FADE, 
                 auto_play_interval=3, on_change=None, width=None, height=None):
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
        
        

        # Progress bars for each screen
        self.progress_bars = [
            ft.ProgressBar(value=1.0 if i == 0 else 0.0, expand=True,bgcolor="black",color="white")
            for i in range(len(screens))
        ]
        self.progress_row = ft.Row(
            self.progress_bars,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        # Initialize Column with width and height
        super().__init__(
    controls=[
        ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=self.switcher,
                        expand=True,
                      
                    ),
                    ft.Container(
                        content=self.progress_row,
                        alignment=ft.alignment.bottom_center,
                        margin=10
                    )
                ],
                expand=True
            ),
            expand=True,
            alignment=ft.alignment.center,
            margin=0,
            bgcolor="transparent",
        ),
    ],
    width=width,
    height=height,
    alignment=ft.MainAxisAlignment.CENTER
)

    def update_progress_bars(self):
        # Update progress bar values based on current index
        for i, progress_bar in enumerate(self.progress_bars):
            progress_bar.value = 1.0 if i == self.current_index else 0.0
            progress_bar.update()

    def did_mount(self):
        # Start auto-play when widget is mounted
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
        self.is_auto_play = False
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
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?1", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?2", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?3", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?1", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?2", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?3", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?1", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?2", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?3", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?1", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?2", fit=ft.ImageFit.COVER, expand=True))),
#     ScreenWidget(image_box=Image_Box(ft.Image(src="https://picsum.photos/200/200?3", fit=ft.ImageFit.COVER, expand=True))),
# ]

#     carousel = CarouselWidget(
#         screens=screens,
#         animation_type=ft.AnimatedSwitcherTransition.FADE,
#         auto_play_interval=3,
#         on_change=lambda index: print(f"Current screen: {index}"),
#         width=400,
#         height=300
#     )

#     page.add(carousel)

# ft.app(target=main)