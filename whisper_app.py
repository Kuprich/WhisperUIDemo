import flet as ft


class WhisperApp(ft.UserControl):
    BUTTON_WIDTH = 150

    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self._configure_window()
        self._configure_file_picker()

        self._build_components()
        self._add_components_to_page()

        self.page.update()

    def build(self):
        return ft.Container()

    def _on_dialog_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_file.value = e.files[0].name
            self.page.update()

    def _recognize_button_click(self, e):
        self.result_text_field.value = "recognize_button_clicked"
        self.page.update()

    def _configure_window(self):
        self.page.window_height = 500
        self.page.window_width = 800
        self.page.window_center()

    def _build_components(self):
        self.file_button = self._build_file_button()
        self.model_dropdown = self._build_model_dropdown()
        self.recognize_button = self._build_recognize_button()
        self.selected_file = self._build_selected_file()
        self.result_text_field = self._build_result_text_field()

    def _add_components_to_page(self):
        self.page.add(
            ft.Row(
                [
                    self.file_button,
                    self.selected_file,
                ]
            ),
            ft.Row([self.recognize_button, self.model_dropdown]),
            ft.Container(padding=1),
            ft.Row([self.result_text_field], expand=True),
        )

    def _configure_file_picker(self):
        self.file_picker = ft.FilePicker(on_result=self._on_dialog_result)
        self.page.overlay.append(self.file_picker)

    def _build_file_button(self):
        return ft.FloatingActionButton(
            content=ft.Row(
                [ft.Icon(ft.icons.AUDIO_FILE_OUTLINED), ft.Text("Select audio file")],
                alignment="center",
                spacing=5,
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=False),
            width=self.BUTTON_WIDTH,
        )

    def _build_model_dropdown(self):
        return ft.Dropdown(
            label="Model",
            width=self.BUTTON_WIDTH,
            options=[
                ft.dropdown.Option("Tiny"),
                ft.dropdown.Option("Base"),
                ft.dropdown.Option("Small"),
                ft.dropdown.Option("Medium"),
                ft.dropdown.Option("Large"),
            ],
            value="Base",
        )

    def _build_recognize_button(self):
        return ft.FloatingActionButton(
            content=ft.Row(
                [ft.Icon(ft.icons.TEXT_ROTATION_NONE), ft.Text("Recognize")],
                alignment="center",
                spacing=5,
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            on_click=self._recognize_button_click,
            width=self.BUTTON_WIDTH,
        )

    def _build_selected_file(self):
        return ft.TextField(label="Selected file", disabled=True, expand=True)

    def _build_result_text_field(self):
        return ft.TextField(
            multiline=True,
            expand=True,
            min_lines=20,
            hint_text="Recognition result",
            read_only=True,
        )
