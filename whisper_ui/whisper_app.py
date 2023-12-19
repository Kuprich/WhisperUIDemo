import flet as ft
import whisper_service.whisper_service as whisper_service
from whisper_ui.whisper_control import WhisperControl
from whisper_ui.whisper_output_control import WhisperOutputControl


class WhisperApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self._configure_window()

        self.whisper_control = WhisperControl(self.page, self.recognize_button_clicked)
        self.whisper_output_control = WhisperOutputControl()
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
                ft.Tab(text="Output", content=self.whisper_output_control),
            ],
            expand=True,
        )

    def recognize_button_clicked(self, e):
        self.whisper_control.result = ""
        self.whisper_output_control.result = ""
        self.whisper_control.is_whisper_running = True
        whisper_service.recognize(
            audio=self.whisper_control.audio_path,
            model_name=self.whisper_control.model_name,
            partial_result_received=self.partial_result_received,
            output_data_received=self.output_data_received,
        )
        self.whisper_control.is_whisper_running = False

    def partial_result_received(self, partial_result: str):
        if self.whisper_control.result == "":
            self.whisper_control.result = partial_result.lstrip()
        else:
            self.whisper_control.result += partial_result

    def output_data_received(self, partial_output_data: str):
        self.whisper_output_control.result += partial_output_data + "\n"
