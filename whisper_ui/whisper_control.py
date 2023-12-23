import flet as ft
import pyperclip
from  whisper_ui.whisper_output_control import WhisperOutputControl


class WhisperControl(ft.UserControl):
    BUTTON_WIDTH = 150
    FILE_EXTENSIONS = ["wav", "mp3"]
    DEFAULT_TIME_VALUE = "00:00"

    def __init__(self, page: ft.Page, output_control: WhisperOutputControl, recognize_button_clicked):
        super().__init__()
        self.recognize_button_clicked = recognize_button_clicked
        self.page = page
        self.output_control = output_control
        self._audio_path = ""
        self._result = ""
        self._time_processed = self.DEFAULT_TIME_VALUE
        self._is_whisper_running = False
        self._build_controls()

    @property
    def audio_path(self):
        """Path of the selected audio file."""
        return self._audio_path

    @audio_path.setter
    def audio_path(self, value: str):
        self._audio_path = value
        self.selected_text_field.value = value
        self.recognize_button.disabled = value == ""
        self.update()

    @property
    def result(self):
        """Recognition rezult, returned whisper service."""
        return self._result

    @result.setter
    def result(self, value: str):
        self._result = value
        self.result_text_field.value = value
        if self._result:
            self.copy_button.disabled = False
        else:
            self.copy_button.disabled = True
        self.update()

    @property
    def is_whisper_running(self):
        """True, if whisper recognition process running"""
        return self._is_whisper_running

    @is_whisper_running.setter
    def is_whisper_running(self, value: bool):
        self._is_whisper_running = value
        if value:
            self.result = ""
            self.output_control.result = ""
            self.progress_ring.visible = True
            self.recognize_button.disabled = True
            self.file_button.disabled = True
            self.model_dropdown.disabled = True
        else:
            self.progress_ring.visible = False
            self.recognize_button.disabled = False
            self.file_button.disabled = False
            self.model_dropdown.disabled = False
            self.bottom_sheet.open = True
            self.time_processed = self.DEFAULT_TIME_VALUE
            self.page.update()
        self.update()

    @property
    def time_processed(self):
        """Property shows how much time is recognized"""
        return self._time_processed

    @time_processed.setter
    def time_processed(self, value: str):
        self._time_processed = value
        self.time_processed_text.value = value
        self.update()

    @property
    def model_name(self):
        """Whisper model name"""
        return self.model_dropdown.value.lower()

    def _build_controls(self):
        self.file_button = self._build_file_button()
        self.selected_text_field = self._build_selected_file()
        self.model_dropdown = self._build_model_dropdown()
        self.recognize_button = self._build_recognize_button()
        self.time_processed_text = self._buid_time_processed_text()
        self.progress_ring = self._build_progress_ring()
        self.result_text_field = self._build_result_text_field()
        self.copy_button = self._build_copy_button()
        self.page.snack_bar = self._build_snack_bar()
        self.bottom_sheet = self._build_bottom_sheet()
        self.page.overlay.append(self.bottom_sheet)
        self._configure_file_picker()

    def build(self):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([self.file_button, self.selected_text_field]),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            self.recognize_button,
                                            self.model_dropdown,
                                            self.progress_ring,
                                        ],
                                    ),
                                    ft.Container(
                                        self.copy_button, margin=ft.margin.only(right=3)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ]
                    ),
                    padding=ft.padding.only(top=10, bottom=5),
                ),
                ft.Row([self.result_text_field], expand=True),
            ]
        )

    def _build_model_dropdown(self):
        return ft.Dropdown(
            label="Model",
            width=self.BUTTON_WIDTH,
            options=[
                ft.dropdown.Option("tiny.en"),
                ft.dropdown.Option("tiny"),
                ft.dropdown.Option("base.en"),
                ft.dropdown.Option("base"),
                ft.dropdown.Option("small.en"),
                ft.dropdown.Option("small"),
                ft.dropdown.Option("medium.en"),
                ft.dropdown.Option("medium"),
                ft.dropdown.Option("large"),
                ft.dropdown.Option("large-v1"),
                ft.dropdown.Option("large-v2"),
                ft.dropdown.Option("large-v3"),
            ],
            value="base",
            tooltip="Select whisper recognition model",
        )

    def _build_recognize_button(self):
        return ft.FloatingActionButton(
            content=ft.Row(
                [ft.Icon(ft.icons.TEXT_ROTATION_NONE), ft.Text("Recognize")],
                alignment="center",
                spacing=5,
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            on_click=self._recognize_button_on_click,
            width=self.BUTTON_WIDTH,
            disabled=True,
            tooltip="Start recognition Process",
        )

    def _build_result_text_field(self):
        return ft.TextField(
            multiline=True,
            expand=True,
            min_lines=40,
            hint_text="Recognition result",
            read_only=True,
        )

    def _build_file_button(self):
        return ft.FloatingActionButton(
            content=ft.Row(
                [ft.Icon(ft.icons.AUDIO_FILE_OUTLINED), ft.Text("Select audio file")],
                alignment="center",
                spacing=5,
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            on_click=lambda _: self.file_picker.pick_files(
                allow_multiple=False, allowed_extensions=self.FILE_EXTENSIONS
            ),
            width=self.BUTTON_WIDTH,
            tooltip="Select audio from FileExplorer",
        )

    def _build_selected_file(self):
        return ft.TextField(label="Selected file", disabled=True, expand=True)

    def _build_progress_ring(self):
        progress_ring = ft.Container(
            ft.ProgressRing(width=20, height=20, stroke_width=2),
            margin=ft.margin.only(left=20, right=10),
        )
        return ft.Row(
            [
                progress_ring,
                ft.Column(
                    [
                        ft.Text("Please wait..."),
                        ft.Row(
                            [
                                ft.Text("Already recognized:"),
                                self.time_processed_text,
                            ]
                        ),
                    ],
                ),
            ],
            visible=False,
        )

    def _buid_time_processed_text(self):
        return ft.Text(self.time_processed)

    def _build_copy_button(self):
        return ft.FloatingActionButton(
            icon=ft.icons.COPY_ALL_OUTLINED,
            on_click=self._copy_button_click,
            bgcolor=ft.colors.YELLOW_100,
            tooltip="Copy all text from result area",
            disabled=True,
        )

    def _build_snack_bar(self):
        return ft.SnackBar(
            content=ft.Text(
                "Result copied to Clipboard!", color=ft.colors.ON_PRIMARY_CONTAINER
            ),
            action="Alright!",
            bgcolor=ft.colors.YELLOW_100,
            action_color=ft.colors.ON_PRIMARY_CONTAINER,
        )

    def _build_bottom_sheet(self):
        return ft.BottomSheet(
            ft.Container(
                ft.Row(
                    [
                        ft.Text("Recognition process finished!", expand=True),
                        ft.ElevatedButton("OK", on_click=self._bottom_sheet_ok_click),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10, horizontal=20),
            ),
        )

    def _bottom_sheet_ok_click(self, e):
        self.bottom_sheet.open = False
        self.page.update()

    def _configure_file_picker(self):
        self.file_picker = ft.FilePicker(on_result=self._on_dialog_result)
        self.page.overlay.append(self.file_picker)

    def _on_dialog_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.audio_path = e.files[0].path

    def _copy_button_click(self, e):
        pyperclip.copy(self.result)
        self.page.snack_bar.open = True
        self.page.update()
        
    def _recognize_button_on_click(self, e):
        self.is_whisper_running = True
        self.recognize_button_clicked(e)
        self.is_whisper_running = False
