import flet as ft


def main(page: ft.Page):
    BUTTON_WIDTH = 150

    page.window_height = 500
    page.window_width = 800

    page.window_center()

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file.value = e.files[0].name
            page.update()

    def recognize_button_click(e):
        result.value = "recognize_button_clicked"
        page.update()

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    file_button = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.AUDIO_FILE_OUTLINED), ft.Text("Select audio file")],
            alignment="center",
            spacing=5,
        ),
        shape=ft.RoundedRectangleBorder(radius=5),
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
        width=BUTTON_WIDTH,
    )

    recognize_button = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.TEXT_ROTATION_NONE), ft.Text("Recognize")],
            alignment="center",
            spacing=5,
        ),
        shape=ft.RoundedRectangleBorder(radius=5),
        on_click=recognize_button_click,
        width=BUTTON_WIDTH,
    )

    whisper_model_dropdown = ft.Dropdown(
        label="Model",
        width=BUTTON_WIDTH,
        options=[
            ft.dropdown.Option("Tiny"),
            ft.dropdown.Option("Base"),
            ft.dropdown.Option("Small"),
            ft.dropdown.Option("Medium"),
            ft.dropdown.Option("Large"),
        ],
        value="Base",
    )

    selected_file = ft.TextField(label="Selected file", disabled=True, expand=True)
    result = ft.TextField(
        multiline=True,
        expand=True,
        min_lines=50,
        hint_text="Recognition result",
        read_only=True,
    )

    page.add(
        ft.Row(
            controls=[
                file_button,
                selected_file,
            ]
        ),
        ft.Row([recognize_button, whisper_model_dropdown]),
        ft.Container(padding=1),
        ft.Row([result], expand=True),
    )

    page.update()


ft.app(target=main)
