import flet as ft

MAX_WIDTH = 250

# Custom Card-like wrapper with limited, enforced properties
def LevelCard(content, bgcolor=None, padding=20, border_radius=10):
    return ft.Container(
        content=content,
        bgcolor=bgcolor,
        padding=padding,
        border_radius=border_radius,
        width=MAX_WIDTH,
        alignment=ft.alignment.center
    )

# Layout class that uses MyCard widgets
class CenteredLayout:
    def __init__(self, page: ft.Page, width: int = 300, controls=None):
        self.page = page
        self.width = width
        self.controls = controls if controls else []
        self.create_controls()

    def create_controls(self):
        column = ft.Column(spacing=20, width=self.width)

        for i, control in enumerate(self.controls):
            alignment = ft.MainAxisAlignment.START if i % 2 == 0 else ft.MainAxisAlignment.END
            row = ft.Row(
                controls=[control],
                alignment=alignment
            )
            column.controls.append(row)

        self.page.add(column)

# # App entry
# def main(page: ft.Page):
#     page.horizontal_alignment = "center"
#     page.scroll  =True
#     layout = CenteredLayout(
#         page,
#         width=500,
#         controls=[
#             LevelCard(
#                 content=ft.Column([
#                     ft.Text("Level 1: Beginner", size=20, weight=ft.FontWeight.BOLD),
#                     ft.Text("Start your journey here."),
#                     ft.Text("Access basic tutorials and guides.")
#                 ]),
#                 bgcolor="lightblue"
#             ),
#             LevelCard(
#                 content=ft.Column([
#                     ft.Text("Level 2: Intermediate", size=20, weight=ft.FontWeight.BOLD),
#                     ft.Text("Take it up a notch."),
#                     ft.Text("Unlock challenges and personalized learning.")
#                 ]),
#                 bgcolor="lightgreen"
#             ),
#             LevelCard(
#                 content=ft.Column([
#                     ft.Text("Level 3: Advanced", size=20, weight=ft.FontWeight.BOLD),
#                     ft.Text("Get into expert territory."),
#                     ft.Text("Includes mentorship and networking.")
#                 ]),
#                 bgcolor="lightcoral"
#             ),
#         ]
#     )

# ft.app(target=main)
