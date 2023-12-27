import flet as ft

BUTTON_HEIGHT = 54
BUTTON_WIDTH = 150


def build_elevated_button(
    text: str = "",
    icon: str = None,
    tooltip: str = None,
    on_click=None,
    disabled: bool = None,
):
    return ft.ElevatedButton(
        text=text,
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
    disabled: bool = None,
    icon_color: str = None,
):
    return ft.IconButton(
        icon=icon,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=15),
        height=BUTTON_HEIGHT,
        on_click=on_click,
        tooltip=tooltip,
        disabled=disabled,
        icon_color=icon_color,
    )


def build_recognize_button(on_click=None, disabled=None):
    recognize_button = build_elevated_button(
        text="Recognize",
        icon=ft.icons.TEXT_ROTATION_NONE,
        tooltip="Start recognition Process",
        on_click=on_click,
        disabled=disabled,
    )
    recognize_button.disabled = True
    recognize_button.width = BUTTON_WIDTH
    return recognize_button


def _build_model_dropdown():
    return ft.Dropdown(
        label="Model",
        width=BUTTON_WIDTH,
        options=[
            ft.dropdown.Option("tiny.en"),
            ft.dropdown.Option("tiny"),
            ft.dropdown.Option("base.en"),
            ft.dropdown.Option("base"),
            ft.dropdown.Option("small.en"),
            ft.dropdown.Option("small"),
            ft.dropdown.Option("medium.en"),
            ft.dropdown.Option("medium"),
            ft.dropdown.Option("large"),
            ft.dropdown.Option("large-v1"),
            ft.dropdown.Option("large-v2"),
            ft.dropdown.Option("large-v3"),
        ],
        value="base",
        tooltip="Select whisper recognition model",
    )


def build_progress_ring(processed_value: ft.Control):
    progress_ring = ft.Container(
        ft.ProgressRing(width=20, height=20, stroke_width=2),
        margin=ft.margin.only(left=20, right=10),
    )
    return ft.Row(
        [
            progress_ring,
            ft.Column(
                [
                    ft.Text("Please wait..."),
                    ft.Row(
                        [
                            ft.Text("Already recognized:"),
                            processed_value,
                        ]
                    ),
                ],
            ),
        ],
        visible=False,
    )
