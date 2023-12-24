import flet as ft


class WhisperBatchControl(ft.UserControl):
    def __init__(self, get_directory_dialog: ft.FilePicker):
        super().__init__()
        self.get_directory_dialog = get_directory_dialog
        self.get_directory_dialog.on_result = self._get_directory_result
        self.select_output_folder_button = self._build_select_output_folder_button()
        self.output_folder_text_field = self._build_output_folder_text_field()

    def build(self):
        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.select_output_folder_button,
                            self.output_folder_text_field,
                        ]
                    )
                ]
            ),
            padding=ft.padding.only(top=10),
        )

    def _build_select_output_folder_button(self):
        return ft.FloatingActionButton(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.DRIVE_FOLDER_UPLOAD),
                    ft.Text("Select output folder"),
                ],
                alignment="center",
                spacing=5,
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            on_click=lambda _: self.get_directory_dialog.get_directory_path(),
            width=170,
            tooltip="Select audio from FileExplorer",
        )

    def _build_output_folder_text_field(self):
        return ft.TextField(label="Selected folder", disabled=True, expand=True)

    def _get_directory_result(self, e: ft.FilePickerResultEvent):
        e.path if e.path else "Cancelled!"
