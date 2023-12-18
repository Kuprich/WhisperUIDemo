import flet as ft


class WhisperOutputControl(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.output_text_filed = ft.TextField(
            min_lines=100,
            hint_text="Output from the whisper service",
            expand=True,
            multiline=True,
            read_only=True,
        )

    def build(self):
        return ft.Container(
            content=ft.Row([self.output_text_filed], expand=True),
            padding=ft.padding.only(top=10),
        )
