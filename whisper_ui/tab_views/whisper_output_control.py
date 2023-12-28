import flet as ft


class WhisperOutputControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self._result = ""
        self.output_text_filed = self._build_output_text_field()

    @property
    def result(self):
        """Output data for whisper transcribe method."""
        return self._result

    @result.setter
    def result(self, value: str):
        self._result = value
        self.output_text_filed.value = value
        self.update()

    def build(self):
        return ft.Container(
            content=ft.Row([self.output_text_filed], expand=True),
            padding=ft.padding.only(top=10),
        )

    def _build_output_text_field(self):
        return ft.TextField(
            min_lines=100,
            hint_text="Output from the whisper service",
            expand=True,
            multiline=True,
            read_only=True,
            text_size=13,
        )
