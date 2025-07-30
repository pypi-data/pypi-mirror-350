import flet as ft

class ScreenWidget:
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

class OnboardingWidget(ft.Column):
    def __init__(self, screens, animation_type=ft.AnimatedSwitcherTransition.FADE, on_skip=None, on_next=None, on_finish=None):
        self.screens = screens
        self.on_skip = on_skip
        self.on_next = on_next
        self.on_finish = on_finish
        self.current_index = 0
        self.switcher = ft.AnimatedSwitcher(
            content=self.screens[0].build(),
            transition=animation_type,
            duration=600,
            reverse_duration=600,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
            expand=True
        )
        
        # Create buttons with initial visibility
        self.skip_button = ft.TextButton(
            "Skip",
            on_click=self.skip,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.TRANSPARENT
            ),
            visible=len(self.screens) > 1  # Show only if multiple screens
        )
        self.back_button = ft.TextButton(
            "Back",
            on_click=self.back,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.TRANSPARENT
            ),
            visible=False  # Hidden on first screen
        )
        self.next_button = ft.TextButton(
            "Next",
            on_click=self.next,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.TRANSPARENT
            )
        )

        # Initialize Column with content
        super().__init__(
            controls=[
                ft.Container(
                    self.switcher,
                    expand=True,
                    alignment=ft.alignment.center,margin=0
                ),
                ft.Row(
                    [
                        self.skip_button,
                        self.back_button,
                        self.next_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def update_buttons(self):
        # Update button visibility based on current index
        self.back_button.visible = self.current_index > 0
        self.skip_button.visible = self.current_index < len(self.screens) - 1 and len(self.screens) > 1
        self.next_button.text = "Finish" if self.current_index == len(self.screens) - 1 else "Next"
        self.back_button.update()
        self.skip_button.update()
        self.next_button.update()

    def skip(self, e):
        if self.on_skip:
            self.on_skip(e)

    def next(self, e):
        self.current_index += 1
        if self.current_index < len(self.screens):
            self.switcher.content = self.screens[self.current_index].build()
            self.switcher.update()
            self.update_buttons()
            if self.on_next:
                self.on_next(e)
        else:
            if self.on_finish:
                self.on_finish(e)

    def back(self, e):
        if self.current_index > 0:
            self.current_index -= 1
            self.switcher.content = self.screens[self.current_index].build()
            self.switcher.update()
            self.update_buttons()

# def main(page: ft.Page):
#     page.title = "Onboarding Screen"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
#     page.window.always_on_top = True
#     page.theme_mode  ="light"
#     page.padding = 0

#     screens = [
#         ScreenWidget(
#             controls=[
#                 ft.Text("Welcome to the app!", size=20),
#                 ft.Text("This is the first screen", size=16),
#             ],
#             bgcolor="red"
#         ),
#         ScreenWidget(
#             controls=[
#                 ft.Image(src="https://via.placeholder.com/200", width=200, height=200),
#                 ft.Text("Explore features", size=20),
#                 ft.Text("This is the second screen", size=16),
#             ],
#             bgcolor="blue"
#         )
#     ]

#     onboarding = OnboardingWidget(
#         screens=screens,
#         animation_type=ft.AnimatedSwitcherTransition.FADE,
#         on_skip=lambda e: print("Skipped"),
#         on_next=lambda e: print("Next screen"),
#         on_finish=lambda e: print("Onboarding completed")
#     )

#     page.add(onboarding)

# ft.app(target=main)