import flet as ft
import whisper_service.whisper_service as whisper_service

from whisper_ui.app_tab_control import AppTabControl


class WhisperApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self._configure_window()

        self.pick_files_dialog = ft.FilePicker()
        self.get_directory_dialog = ft.FilePicker()
        
        self.page.snack_bar = ft.SnackBar(ft.Container())
        self.page.bottom_sheet = ft.BottomSheet(ft.Container())
        self.page.overlay.extend([self.pick_files_dialog, self.get_directory_dialog, self.page.bottom_sheet])

        self.tabs = AppTabControl(
            page=page,
            pick_files_dialog=self.pick_files_dialog,
            get_directory_dialog = self.get_directory_dialog,
            snack_bar=self.page.snack_bar,
            recognize_button_clicked=self.recognize_button_clicked,
        )

    def build(self):
        return ft.Container()

    def _configure_window(self):
        self.page.window_height = 700
        self.page.window_width = 1000
        self.page.window_center()

    def recognize_button_clicked(self, e):
        is_success = whisper_service.recognize(
            audio=self.tabs.whisper_single_control.audio_path,
            model_name=self.tabs.whisper_single_control.model_name,
            partial_result_received=self._partial_result_received,
            output_data_received=self._output_data_received,
        )
        return is_success

    def _partial_result_received(self, partial_result: str, time_processed: str):
        if self.tabs.whisper_single_control.result == "":
            self.tabs.whisper_single_control.result = partial_result.lstrip()
        else:
            self.tabs.whisper_single_control.result += partial_result

        self.tabs.whisper_single_control.time_processed = time_processed

    def _output_data_received(self, partial_output_data):
        self.tabs.whisper_output_control.result += partial_output_data + "\n"
