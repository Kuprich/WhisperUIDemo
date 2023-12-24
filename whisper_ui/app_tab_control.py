import flet as ft


class AppTabControl(ft.UserControl):
    def __init__(
        self,
        page,
        whisper_single_control: ft.UserControl,
        whisper_batch_control: ft.UserControl,
        whisper_output_control: ft.UserControl,
    ):
        super().__init__()
        self.page = page
        self.whisper_single_control = whisper_single_control
        self.whisper_batch_control = whisper_batch_control
        self.whisper_output_control = whisper_output_control
        self.popup_menu_button = self._build_popup_menu_button()
        self.main_tab = self._build_main_tab()
        self.tabs = self._build_tabs()
        self.page.add(self.tabs)

    def build(self):
        return ft.Container()

    def _build_tabs(self):
        return ft.Tabs(
            animation_duration=200,
            tabs=[
                self.main_tab,
                ft.Tab(
                    content=self.whisper_output_control, icon=ft.icons.TERMINAL_OUTLINED
                ),
            ],
            expand=True,
        )

    def _build_main_tab(self):
        return ft.Tab(
            tab_content=ft.Row(
                [
                    self.popup_menu_button,
                    ft.Text("Main"),
                ]
            ),
            content=self.whisper_single_control,
        )

    def _build_popup_menu_button(self):
        return ft.PopupMenuButton(
            icon=ft.icons.ARROW_DROP_DOWN,
            items=[
                ft.PopupMenuItem(
                    text="Single file process",
                    checked=True,
                    on_click=self._single_mode_clicked,
                ),
                ft.PopupMenuItem(
                    text="Batch process", on_click=self._batch_mode_clicked
                ),
            ],
            tooltip="Select recognition mode",
        )

    def _single_mode_clicked(self, e):
        for item in self.popup_menu_button.items:
            item.checked = False
        e.control.checked = True
        self.main_tab.content = self.whisper_single_control
        self.page.update()

    def _batch_mode_clicked(self, e):
        for item in self.popup_menu_button.items:
            item.checked = False
        e.control.checked = True
        self.main_tab.content = self.whisper_batch_control
        self.page.update()
