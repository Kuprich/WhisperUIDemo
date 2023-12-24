import flet as ft

BUTTON_HEIGHT = 54


def build_elevated_button(
    text: str = "",
    icon: str = None,
    tooltip: str = None,
    on_click=None,
):
    return ft.ElevatedButton(
        text = text,
        icon=icon,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=15),
        height=BUTTON_HEIGHT,
        on_click=on_click,
        tooltip=tooltip,
    )

def build_icon_button(
    icon: str = None,
    tooltip: str = None,
    on_click=None,
    disabled=None
):
    return ft.IconButton(
        icon=icon,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=15),
        height=BUTTON_HEIGHT,
        on_click=on_click,
        tooltip=tooltip,
        disabled=disabled
    )
