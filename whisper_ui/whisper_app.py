import flet as ft
import whisper_service.whisper_service as whisper_service
from whisper_ui.whisper_single_control import WhisperSingleControl
from whisper_ui.whisper_output_control import WhisperOutputControl
from whisper_ui.whisper_batch_control import WhisperBatchControl


class WhisperApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self._configure_window()

        self.whisper_output_control = WhisperOutputControl()
        self.whisper_single_control = WhisperSingleControl(
            self.page, self.whisper_output_control, self.recognize_button_clicked
        )
        self.whisper_batch_control = WhisperBatchControl()
        self.main_tab = self._build_main_tab()
        self.tabs_control = self._build_tabs_control()

        page.add(self.tabs_control)

    def build(self):
        return ft.Container()

    def _configure_window(self):
        self.page.window_height = 700
        self.page.window_width = 1000
        self.page.window_center()

    def _build_tabs_control(self):
        return ft.Tabs(
            animation_duration=200,
            tabs=[
                self.main_tab,
                ft.Tab(
                    content=self.whisper_output_control, icon=ft.icons.TERMINAL_OUTLINED
                ),
            ],
            expand=True,
        )

    def _build_main_tab(self):
        return ft.Tab(
            tab_content=ft.Row(
                [
                    ft.PopupMenuButton(
                        icon=ft.icons.ARROW_DROP_DOWN,
                        items=[
                            ft.PopupMenuItem(text="Single file process", checked=True, on_click=self._single_mode_clicked),
                            ft.PopupMenuItem(text="Batch process", on_click=self._batch_mode_clicked),
                        ],
                        tooltip="Select recognition mode"
                    ),
                    ft.Text("Main"),
                ]
            ),
            content=self.whisper_single_control,
        )
    
    def _single_mode_clicked(self, e):
        self.main_tab.content = self.whisper_single_control
        self.page.update()
        
    def _batch_mode_clicked(self, e):
        self.main_tab.content = self.whisper_batch_control
        self.page.update()

    def recognize_button_clicked(self, e):
        is_success = whisper_service.recognize(
            audio=self.whisper_single_control.audio_path,
            model_name=self.whisper_single_control.model_name,
            partial_result_received=self.partial_result_received,
            output_data_received=self.output_data_received,
        )
        return is_success

    def partial_result_received(self, partial_result: str, time_processed: str):
        if self.whisper_single_control.result == "":
            self.whisper_single_control.result = partial_result.lstrip()
        else:
            self.whisper_single_control.result += partial_result

        self.whisper_single_control.time_processed = time_processed

    def output_data_received(self, partial_output_data):
        self.whisper_output_control.result += partial_output_data + "\n"
