import flet as ft
from pathlib import Path
import os
import whisper_service.whisper_service as whisper_service

from whisper_ui.app_tab_control import AppTabControl


class WhisperApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self._configure_window()

        self.pick_files_dialog_single = ft.FilePicker()
        self.pick_files_dialog_batch = ft.FilePicker()
        self.get_directory_dialog_batch = ft.FilePicker()

        self.page.snack_bar = ft.SnackBar(ft.Container())
        self.page.bottom_sheet = ft.BottomSheet(ft.Container())
        self.page.overlay.extend(
            [
                self.pick_files_dialog_single,
                self.pick_files_dialog_batch,
                self.get_directory_dialog_batch,
                self.page.bottom_sheet,
            ]
        )

        self.tabs = AppTabControl(
            page=page,
            pick_files_dialog_single=self.pick_files_dialog_single,
            pick_files_dialog_batch=self.pick_files_dialog_batch,
            get_directory_dialog_batch=self.get_directory_dialog_batch,
            snack_bar=self.page.snack_bar,
            recognize_button_single_clicked=self._recognize_button_single_clicked,
            recognize_button_batch_clicked=self._recognize_button_batch_clicked,
        )

    def build(self):
        return ft.Container()

    def _configure_window(self):
        self.page.window_height = 700
        self.page.window_width = 1000
        self.page.window_center()

    def _disable_popup(self):
        self.tabs.popup_menu_button.disabled = True
        self.page.update()

    def _enable_popup(self):
        self.tabs.popup_menu_button.disabled = False
        self.page.update()

    def _recognize_button_single_clicked(self, e):
        self.tabs.whisper_output_control.result = ""
        self._disable_popup()
        result = whisper_service.recognize(
            audio=self.tabs.whisper_single_control.audio_path,
            model_name=self.tabs.whisper_single_control.model_name,
            partial_result_received=self.tabs.whisper_single_control.partial_result_received,
            output_data_received=self._output_data_received,
        )
        self._enable_popup()
        return result.is_success

    def _recognize_button_batch_clicked(self, e):
        def _get_processed_value(current, total):
            return f"{current} out of {total}"

        self.tabs.whisper_output_control.result = ""
        self._disable_popup()
        current = 0
        total = len(self.tabs.whisper_batch_control.uploaded_files)
        self.tabs.whisper_batch_control.processed_value = _get_processed_value(
            current, total
        )
        for audio_path in self.tabs.whisper_batch_control.uploaded_files:
            self.tabs.whisper_batch_control.file_in_process(audio_path)
            result = whisper_service.recognize(
                audio_path,
                model_name=self.tabs.whisper_batch_control.model_name,
                output_data_received=self._output_data_received,
            )

            if result.is_success:
                filename = Path(audio_path).stem + ".txt"
                file_path = os.path.join(
                    self.tabs.whisper_batch_control.output_folder, filename
                )
                try:
                    with open(file_path, "w") as file:
                        file.write(result.text)
                except Exception as e:
                    self._output_data_received(partial_output_data=str(e))
                self.tabs.whisper_batch_control.file_recognized(audio_path, file_path)
            else:
                break
                
            current += 1
            self.tabs.whisper_batch_control.processed_value = _get_processed_value(
                current, total
            )

        self._enable_popup()

    def _output_data_received(self, partial_output_data):
        self.tabs.whisper_output_control.result += partial_output_data + "\n"
