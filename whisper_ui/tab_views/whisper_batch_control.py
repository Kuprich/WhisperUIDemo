import os
import flet as ft
import whisper_ui.shared_controls as shared_controls
from whisper_ui.audio_list import AudioListContentControl


class WhisperBatchControl(ft.UserControl):
    FILE_EXTENSIONS = ["wav", "mp3"]
    BOTTOM_SHEET_TEXT = "Recognition process finished!"

    def __init__(
        self,
        page: ft.Page,
        get_directory_dialog: ft.FilePicker,
        pick_files_dialog: ft.FilePicker,
        recognize_button_clicked,
    ):
        super().__init__()
        self.page = page
        self._processed_value = ""
        self._output_folder = ""
        self._audio_list = AudioListContentControl(
            on_delete_item=self._audio_list_item_deleted,
            on_copy_result=self._recognition_result_copied
        )

        self.recognize_button_clicked = recognize_button_clicked
        self.get_directory_dialog = get_directory_dialog
        self.get_directory_dialog.on_result = self._get_directory_result
        self.pick_files_dialog = pick_files_dialog
        self.pick_files_dialog.on_result = self._pick_files_result

        self.select_output_folder_button = self._build_select_output_folder_button()
        self.output_folder_text_field = self._build_output_folder_text_field()
        self.load_audio_button = self._build_load_audio_button()
        self.recognize_button = self._build_recognize_button()
        self.processed_value_text = self._build_processed_text()
        self.progress_ring = self._build_progress_ring()
        self.model_dropdown = self._build_model_dropdown()
        self.remove_all_button = self._build_remove_all_button()

        self.audio_list_control = self._build_audio_list_control(
            self.audio_list.controls,
        )
        self._configure_snack_bar()

    @property
    def processed_value(self):
        return self._processed_value

    @processed_value.setter
    def processed_value(self, value: str):
        self._processed_value = value
        self.processed_value_text.value = value
        self.update()

    @property
    def audio_list(self):
        return self._audio_list

    def _clear_audio_list(self):
        self.audio_list_control.controls = self._audio_list.clear_audio_list()
        self._set_remove_all_button_activity()
        self._set_recognize_button_activity()
        self.update()

    def _update_audio_list_with_buttons(self):
        self.audio_list_control.controls = self._audio_list.controls
        self._set_remove_all_button_activity()
        self._set_recognize_button_activity()
        self.update()

    def _update_audio_list_without_buttons(self):
        self.audio_list_control.controls = self._audio_list.controls
        self.update()

    def _extend_audio_list(self, value: list[str]):
        self.audio_list_control.controls = self._audio_list.extend(value)
        self._set_remove_all_button_activity()
        self._set_recognize_button_activity()
        self.update()

    def _disable_delete_icon_in_audio_list(self):
        self.audio_list_control.controls = self.audio_list.disable_delete_icon()
        self.update()

    def _enable_delete_icon_in_audio_list(self):
        self.audio_list_control.controls = self.audio_list.enable_delete_icon()
        self.update()

    def _reset_statuses_in_audio_list(self):
        self.audio_list_control.controls = self.audio_list.reset_file_statuses()
        self.update()

    def _build_bottom_sheet_content(self, text):
        return ft.Container(
            ft.Row(
                [
                    ft.Text(text, expand=True, text_align=ft.TextAlign.CENTER),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Open Containing Folder",
                                on_click=self._bottom_sheet_open_folder_click,
                            ),
                            ft.ElevatedButton(
                                "OK", on_click=self._bottom_sheet_ok_click
                            ),
                        ]
                    ),
                ],
            ),
            padding=ft.padding.symmetric(vertical=10, horizontal=20),
        )

    def _bottom_sheet_ok_click(self, e):
        self.page.bottom_sheet.open = False
        self.page.update()

    def _bottom_sheet_open_folder_click(self, e):
        path = self.output_folder
        os.startfile(path)

    def _set_recognize_button_activity(self):
        self.recognize_button.disabled = (
            len(self.uploaded_files) == 0 or self.output_folder == ""
        )

    def _set_remove_all_button_activity(self):
        self.remove_all_button.disabled = len(self.audio_list.files) == 0

    def _configure_snack_bar(self):
        return shared_controls.configure_snack_bar(self.page.snack_bar)

    @property
    def output_folder(self):
        """Folder path where the result will be saved"""
        return self._output_folder

    @output_folder.setter
    def output_folder(self, value: str):
        if value != "":
            self._output_folder = value
            self.output_folder_text_field.value = value
            self._set_recognize_button_activity()
            self.update()

    @property
    def model_name(self):
        """Wshisper recognition model"""
        return self.model_dropdown.value.lower()

    @property
    def uploaded_files(self):
        return self.audio_list.files

    def build(self):
        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.select_output_folder_button,
                            self.output_folder_text_field,
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    self.load_audio_button,
                                    self.recognize_button,
                                    self.model_dropdown,
                                    self.progress_ring,
                                ],
                                expand=True,
                            ),
                            ft.Row([self.remove_all_button]),
                        ]
                    ),
                    ft.Row([self.audio_list_control], expand=True),
                ]
            ),
            padding=ft.padding.only(top=10),
        )

    def _build_select_output_folder_button(self):
        return shared_controls.build_elevated_button(
            text="Select output folder",
            icon=ft.icons.DRIVE_FOLDER_UPLOAD,
            tooltip="Select output folder where the result will be saved",
            on_click=lambda _: self.get_directory_dialog.get_directory_path(),
        )

    def _build_load_audio_button(self):
        return shared_controls.build_elevated_button(
            text="Load audio",
            icon=ft.icons.AUDIO_FILE_OUTLINED,
            on_click=lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=True, allowed_extensions=self.FILE_EXTENSIONS
            ),
        )

    def _build_recognize_button(self):
        return shared_controls.build_recognize_button(
            on_click=self._recognize_button_on_click, disabled=True
        )

    def _recognize_button_on_click(self, e):
        self._whisper_service_started()
        self.recognize_button_clicked(e)
        self._whisper_service_finished()
        return

    def _whisper_service_started(self):
        self._disable_delete_icon_in_audio_list()
        self._reset_statuses_in_audio_list()
        self.progress_ring.visible = True
        self.select_output_folder_button.disabled = True
        self.recognize_button.disabled = True
        self.load_audio_button.disabled = True
        self.model_dropdown.disabled = True
        self.remove_all_button.disabled = True
        self.update()

    def _whisper_service_finished(self):
        self.audio_list.enable_delete_icon()
        self.audio_list_control.controls = self.audio_list.controls
        self.progress_ring.visible = False
        self.select_output_folder_button.disabled = False
        self.recognize_button.disabled = False
        self.load_audio_button.disabled = False
        self.model_dropdown.disabled = False
        self.remove_all_button.disabled = False
        self.page.bottom_sheet.content = self._build_bottom_sheet_content(
            self.BOTTOM_SHEET_TEXT
        )
        self.page.bottom_sheet.open = True
        self.update()
        self.page.update()

    def _build_progress_ring(self):
        return shared_controls.build_progress_ring(self.processed_value_text)

    def _build_processed_text(self, value: str = ""):
        return ft.Text(value)

    def _build_model_dropdown(self):
        return shared_controls.build_model_dropdown()

    def _build_remove_all_button(self):
        return shared_controls.build_icon_button(
            ft.icons.PLAYLIST_REMOVE_OUTLINED,
            tooltip="Remove all uploaded files",
            icon_color=ft.colors.RED_300,
            disabled=True,
            on_click=self._remove_all_button_click,
        )

    def _remove_all_button_click(self, e):
        self._clear_audio_list()

    def _build_output_folder_text_field(self):
        return ft.TextField(label="Selected folder", disabled=True, expand=True)

    def _get_directory_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.output_folder = e.path

    def _pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            files = []
            for file in e.files:
                if file.path not in self.uploaded_files:
                    files.append(file.path)

            self._extend_audio_list(files)

    def _build_audio_list_control(self, controls: list[ft.Control]):
        return ft.ListView(
            controls=controls,
            spacing=10,
            expand=True,
            padding=ft.padding.only(top=10, right=10),
            divider_thickness=0.5,
        )

    def _audio_list_item_deleted(self):
        self._update_audio_list_with_buttons()
        
    def _recognition_result_copied(self):
        self.page.snack_bar.open = True
        self.page.update()

    def file_recognized(self, audio_path: str, output_file_path:str):
        self.audio_list.mark_file_as_recognized(audio_path, output_file_path)
        self._update_audio_list_without_buttons()

    def file_in_process(self, audio_path: str):
        self.audio_list.mark_file_as_in_process(audio_path)
        self._update_audio_list_without_buttons()
