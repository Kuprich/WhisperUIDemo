import flet as ft
import whisper_ui.shared_controls as shared_controls


class WhisperBatchControl(ft.UserControl):
    FILE_EXTENSIONS = ["wav", "mp3"]

    def __init__(
        self, get_directory_dialog: ft.FilePicker, pick_files_dialog: ft.FilePicker, recognize_button_clicked
    ):
        super().__init__()
        self.recognize_button_clicked = recognize_button_clicked
        self.get_directory_dialog = get_directory_dialog
        self.get_directory_dialog.on_result = self._get_directory_result
        self.pick_files_dialog = pick_files_dialog
        self.pick_files_dialog.on_result = self._pick_files_result

        self.select_output_folder_button = self._build_select_output_folder_button()
        self.output_folder_text_field = self._build_output_folder_text_field()
        self.load_audio_button = self._build_load_audio_button()
        self.recognize_button = self._build_recognize_button()
        self.model_dropdown = self._build_model_dropdown()
        self.remove_all_button = self._build_remove_all_button()

        self.audio_list_view = self._build_audio_list_view()
        self._audio_list = []
        self._output_folder = ""
        

    @property
    def output_folder(self):
        """Folder path where the result will be saved"""
        return self._output_folder

    @output_folder.setter
    def output_folder(self, value: str):
        if value != "":
            self._output_folder = value
            self.output_folder_text_field.value = value
            self.recognize_button.disabled = len(self.audio_list) == 0
            self.update()

    @property
    def audio_list(self):
        return self._audio_list
    
    def _extend_audio_list(self, value: list):
        self.audio_list.extend(value)
        self._audio_list_modified()
    
    def _clear_audio_list(self):
        self.audio_list.clear()
        self._audio_list_modified()
        
    def _remove_audio_list_item(self, item:str):
        self._audio_list.remove(item)
        self._audio_list_modified()
        
    def _audio_list_modified(self):
        self.audio_list_view.controls = self._build_list_view_controls(self._audio_list)
        self.remove_all_button.disabled = len(self.audio_list) == 0
        self.recognize_button.disabled = len(self.audio_list) == 0 or self.output_folder == ""
        self.update()

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
                                ],
                                expand=True,
                            ),
                            ft.Row([self.remove_all_button]),
                        ]
                    ),
                    ft.Row([self.audio_list_view], expand=True),
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
        
        return

    def _build_model_dropdown(self):
        return shared_controls._build_model_dropdown()

    def _build_remove_all_button(self):
        return shared_controls.build_icon_button(
            ft.icons.PLAYLIST_REMOVE_OUTLINED,
            tooltip="Remove all uploaded files",
            icon_color=ft.colors.RED_300,
            disabled=True,
            on_click=self._remove_all_button_click
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
                if file.path not in self._audio_list:
                    files.append(file.path)
            self._extend_audio_list(files)

    def _build_audio_list_view(self):
        return ft.ListView(
            controls=self._build_list_view_controls(),
            spacing=10,
            expand=True,
            padding=ft.padding.only(top=10, right=10),
            divider_thickness=0.5,
        )

    def _build_list_view_controls(self, items: list = None):
        if items is not None and len(items) != 0:
            return [self._build_list_item(i) for i in items]
        else:
            return [ft.Text("You haven't uploaded any files yet")]

    def _build_list_item(self, file_path):
        return ft.Row(
            [
                ft.Container(
                    ft.Text(file_path), expand=True, padding=ft.padding.only(left=10)
                ),
                ft.Row(
                    [
                        # ft.Icon(name=ft.icons.CHECK, color=ft.colors.GREEN_500),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINED, icon_color=ft.colors.RED_300, data=file_path, on_click=self._delete_audio_button_click
                        ),
                    ]
                ),
            ]
        )
    
    def _delete_audio_button_click(self, e):
        self._remove_audio_list_item(e.control.data)
