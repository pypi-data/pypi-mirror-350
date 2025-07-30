import flet as ft
from custom_flet_components import Router

router = Router()


@router.route("/")
def DefaultPage(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            
        ],
        horizontal_alignment="center",
        vertical_alignment="center",
        bgcolor=ft.Colors.WHITE
    )
    

@router.route("/login")
def LoginPage(page: ft.Page):
    return ft.View(
        route="/login",
        controls=[
            
        ],
        horizontal_alignment="center",
        vertical_alignment="center",
        bgcolor=ft.Colors.WHITE
    )



@router.route("/dashboard",protected=True)
def DashboardPage(page: ft.Page):
    return ft.View(
        route="/dashboard",
        controls=[
            
        ],
        horizontal_alignment="center",
        padding=0,
        scroll=ft.ScrollMode.HIDDEN
    )


def main(page:ft.Page):
    page.title = "Flet Router with Auth Demo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.always_on_top = True
    page.on_view_pop = lambda _: router.pop()
    router.attach(page)
    page.go(router.current_route)
    print(router.current_route)
    print(page.client_storage.get("is_authenticated"))
    auth = page.client_storage.get("is_authenticated")
    #router.logout()

    # if auth:
    #     router.login()
    #     page.go("/dashboard")

   
ft.app(main)