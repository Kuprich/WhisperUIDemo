import os
import flet as ft
import pyperclip


class AudioItem:
    def __init__(
        self,
        file_path: str,
        delete_icon_disabled: bool = False,
        is_recognized: bool = False,
        is_in_process: bool = False,
        
    ):
        self.file_path = file_path
        self.delete_icon_disabled = delete_icon_disabled
        self.is_recognized = is_recognized
        self.is_in_process = is_in_process
        self.output_file_path = ""


class AudioListContentControl:
    def __init__(self, on_delete_item, on_copy_result = None):
        self.on_item_deleted = on_delete_item
        self.on_copy_result = on_copy_result
        self._audio_items: list[AudioItem] = []

    @property
    def files(self):
        return [audio_item.file_path for audio_item in self._audio_items]

    @property
    def controls(self):
        if self._audio_items is not None and len(self._audio_items) != 0:
            return [
                self._build_list_item(audio_item) for audio_item in self._audio_items
            ]
        else:
            return [ft.Text("You haven't uploaded any files yet")]

    def _build_list_item(self, audio_item: AudioItem):
        
        return ft.Row(
            [
                ft.Container(
                    ft.Text(audio_item.file_path, color=ft.colors.GREEN_900 if audio_item.is_recognized else None),
                    expand=True,
                    padding=ft.padding.only(left=10),
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.CONTENT_COPY,
                            icon_color=ft.colors.BLUE_300,
                            data=audio_item.output_file_path,
                            on_click=self._copy_result_button_click,
                            visible=audio_item.is_recognized,
                            tooltip=f"Copy content from file: {os.path.basename(audio_item.output_file_path)}"),
                        
                        ft.ProgressRing(
                            width=16,
                            height=16,
                            stroke_width=2,
                            visible=audio_item.is_in_process,
                            tooltip="Audio file is currently being recognized"
                        ),
                        ft.Icon(
                            name=ft.icons.CHECK,
                            color=ft.colors.GREEN_500,
                            visible=audio_item.is_recognized,
                            tooltip="Recognition process finished"
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINED,
                            icon_color=ft.colors.RED_300,
                            data=audio_item,
                            on_click=self._delete_audio_button_click,
                            disabled=audio_item.delete_icon_disabled,
                            tooltip="Remove audio from list"
                        ),
                    ]
                ),
            ]
        )

    def extend(self, value: list[str]):
        audio_items = [AudioItem(file_path) for file_path in value]
        self._audio_items.extend(audio_items)
        return self.controls

    def clear_audio_list(self):
        self._audio_items.clear()
        return self.controls

    def disable_delete_icon(self):
        for audio_item in self._audio_items:
            audio_item.delete_icon_disabled = True
        return self.controls

    def reset_file_statuses(self):
        for audio_item in self._audio_items:
            audio_item.is_recognized = False
        return self.controls

    def enable_delete_icon(self):
        for audio_item in self._audio_items:
            audio_item.delete_icon_disabled = False

    def _delete_audio_button_click(self, e):
        self._audio_items.remove(e.control.data)
        self.on_item_deleted()
    
    def _copy_result_button_click(self, e):
        with open(e.control.data) as file:
            content = file.read()
        pyperclip.copy(content)
        self.on_copy_result()
        

    def mark_file_as_in_process(self, file_path: str):
        self._find_audio_by_path(file_path).is_in_process = True

    def mark_file_as_recognized(self, file_path: str, output_file_path:str):
        audio_item = self._find_audio_by_path(file_path)
        audio_item.output_file_path = output_file_path
        audio_item.is_in_process = False
        audio_item.is_recognized = True

    def _find_audio_by_path(self, path: str):
        for audio_item in self._audio_items:
            if audio_item.file_path == path:
                return audio_item
