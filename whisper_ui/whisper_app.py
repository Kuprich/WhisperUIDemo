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

    def _build_tabs_control(self):
        return ft.Tabs(
            animation_duration=200,
            tabs=[
                ft.Tab(
                    tab_content=ft.Row(
                        [
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(text="single"),
                                    ft.PopupMenuItem(text="multiple"),
                                ]
                            ),
                            ft.Text("Main"),
                        ]
                    ),
                    content=self.whisper_control,
                ),
                ft.Tab(
                    content=self.whisper_output_control, icon=ft.icons.TERMINAL_OUTLINED
                ),
            ],
            expand=True,
        )

    def menu_button_clicked(self, e):
        pass

    def recognize_button_clicked(self, e):
        is_success = whisper_service.recognize(
            audio=self.whisper_control.audio_path,
            model_name=self.whisper_control.model_name,
            partial_result_received=self.partial_result_received,
            output_data_received=self.output_data_received,
        )
        return is_success

    def partial_result_received(self, partial_result: str, time_processed: str):
        if self.whisper_control.result == "":
            self.whisper_control.result = partial_result.lstrip()
        else:
            self.whisper_control.result += partial_result

        self.whisper_control.time_processed = time_processed

    def output_data_received(self, partial_output_data):
        self.whisper_output_control.result += partial_output_data + "\n"
