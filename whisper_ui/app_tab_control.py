import flet as ft

from whisper_ui.tab_views.whisper_single_control import WhisperSingleControl
from whisper_ui.tab_views.whisper_output_control import WhisperOutputControl
from whisper_ui.tab_views.whisper_batch_control import WhisperBatchControl


class AppTabControl(ft.UserControl):
    def __init__(
        self,
        page: ft.Page,
        pick_files_dialog_single: ft.FilePicker,
        pick_files_dialog_batch: ft.FilePicker,
        get_directory_dialog_batch: ft.FilePicker,
        snack_bar: ft.SnackBar,
        recognize_button_single_clicked,
        recognize_button_batch_clicked,
    ):
        super().__init__()
        self.page = page

        self.whisper_output_control = WhisperOutputControl()
        self.whisper_single_control = WhisperSingleControl(
            page=page,
            pick_files_dialog=pick_files_dialog_single,
            snack_bar=snack_bar,
            recognize_button_clicked=recognize_button_single_clicked,
        )
        self.whisper_batch_control = WhisperBatchControl(
            page = page,
            get_directory_dialog=get_directory_dialog_batch,
            pick_files_dialog=pick_files_dialog_batch,
            recognize_button_clicked=recognize_button_batch_clicked,
        )
        self.popup_menu_button = self._build_popup_menu_button()
        self.main_tab = self._build_main_tab()
        self.page.add(self._build_tabs())

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

