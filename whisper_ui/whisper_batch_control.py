import flet as ft
class WhisperBatchControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        # self.select_output_folder_button = self._build_select_output_folder_button
        
    def build(self):
        return ft.Column(
            [
                ft.Row([ft.Text("sdf")])
            ]
        )
    
    # def _build_select_output_folder_button(self):
    #     return ft.FloatingActionButton(
    #         content=ft.Row(
    #             [ft.Icon(ft.icons.DRIVE_FOLDER_UPLOAD), ft.Text("Select output folder")],
    #             alignment="center",
    #             spacing=5,
    #         ),
    #         shape=ft.RoundedRectangleBorder(radius=5),
    #         on_click=lambda _: self.file_picker.pid(
    #             allow_multiple=True, allowed_extensions=self.FILE_EXTENSIONS
    #         ),
    #         width=self.BUTTON_WIDTH,
    #         tooltip="Select audio from FileExplorer",
    #     )
    
    