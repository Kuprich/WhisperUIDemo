import flet as ft
from whisper_ui.whisper_control import WhisperControl


class WhisperApp(ft.UserControl):
    BUTTON_WIDTH = 150

    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.selected_file_path = ""

        self._configure_window()

        self.whisper_control = WhisperControl(self.page)
        self.tabs_control = self._build_tabs_control()

        page.add(self.tabs_control)

    def build(self):
        return ft.Container()

    def _configure_window(self):
        self.page.window_height = 510
        self.page.window_width = 800
        self.page.window_center()

    def _build_tabs_control(self):
        return ft.Tabs(
            animation_duration=200,
            tabs=[
                ft.Tab(
                    text="Main",
                    content=self.whisper_control,
                ),
                ft.Tab(
                    text="Output",
                    content=ft.Text("This is Tab 2"),
                ),
            ],
            expand=True,
        )
