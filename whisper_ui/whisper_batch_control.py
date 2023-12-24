import flet as ft
import whisper_ui.shared_controls as shared_controls


class WhisperBatchControl(ft.UserControl):
    FILE_EXTENSIONS = ["wav", "mp3"]

    def __init__(
        self, get_directory_dialog: ft.FilePicker, pick_files_dialog: ft.FilePicker
    ):
        super().__init__()
        self.get_directory_dialog = get_directory_dialog
        self.get_directory_dialog.on_result = self._get_directory_result
        self.pick_files_dialog = pick_files_dialog
        self.pick_files_dialog.on_result = self._pick_files_result
        self.select_output_folder_button = self._build_select_output_folder_button()
        self.output_folder_text_field = self._build_output_folder_text_field()
        # self.load_audio_button = self._build_load_audio_button()

        self._output_folder = ""
        self.audio_files = []

    @property
    def output_folder(self):
        """Folder path where the result will be saved"""
        return self._result

    @output_folder.setter
    def output_folder(self, value: str):
        if value is not "":
            self._output_folder = value
            self.output_folder_text_field.value = value
            self.update()
            
    @property
    def audio_files(self):
        """Loaded audio files"""
        return self._audio_files

    @audio_files.setter
    def audio_files(self, value: list):
        self._audio_files = value
        

    
    

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
                    # ft.Row([self.load_audio_button]),
                ]
            ),
            padding=ft.padding.only(top=10),
        )

    def _build_select_output_folder_button(self):
        return shared_controls.build_elevated_button(
            text="Select output folder",
            icon=ft.icons.DRIVE_FOLDER_UPLOAD,
            tooltip="Select output folder where the result will be saved",
            on_click=lambda _: self.get_directory_dialog.get_directory_path()
        )

    def _build_load_audio_button(self):
        return shared_controls.build_elevated_button(
            text="Load audio",
            icon = ft.icons.AUDIO_FILE_OUTLINED,
            on_click=lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=True, allowed_extensions=self.FILE_EXTENSIONS
            )
        )


    def _build_output_folder_text_field(self):
        return ft.TextField(label="Selected folder", disabled=True, expand=True)

    def _get_directory_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.output_folder = e.path
    
    def _pick_files_result(self, e:ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                self.audio_files.append(file.path)
            
