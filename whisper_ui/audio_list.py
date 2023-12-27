import flet as ft

class AudioItem():
    def __init__(self, file_path:str, delete_icon_disabled:bool = False, success_icon_visible:bool = False):
        self.file_path = file_path
        self.delete_icon_disabled = delete_icon_disabled
        self.success_icon_visible = success_icon_visible


class AudioListContentControl():
    def __init__(self, on_delete_item):
        self.on_item_deleted = on_delete_item
        self._audio_items:list[AudioItem] = []

    @property
    def files(self):
        return [audio_item.file_path for audio_item in self._audio_items]
    
    @property
    def controls(self):
        if self._audio_items is not None and len(self._audio_items) != 0:
            return [self._build_list_item(audio_item) for audio_item in self._audio_items]
        else:
            return [ft.Text("You haven't uploaded any files yet")]
        

    def _build_list_item(self, audio_item:AudioItem):
        return ft.Row(
            [
                ft.Container(
                    ft.Text(audio_item.file_path), expand=True, padding=ft.padding.only(left=10)
                ),
                ft.Row(
                    [
                        ft.Icon(name=ft.icons.CHECK, color=ft.colors.GREEN_500, visible=audio_item.success_icon_visible),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINED,
                            icon_color=ft.colors.RED_300,
                            data=audio_item,
                            on_click=self._delete_audio_button_click,
                            disabled=audio_item.delete_icon_disabled
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
            audio_item.success_icon_visible = False
        return self.controls
    
    def enable_delete_icon(self):
        for audio_item in self._audio_items:
            audio_item.delete_icon_disabled = False

    def _delete_audio_button_click(self, e):
        self._audio_items.remove(e.control.data)
        self.on_item_deleted()
        
    def mark_file_as_recognized(self, file_path:str):
        for audio_item in self._audio_items:
            if audio_item.file_path == file_path:
                audio_item.success_icon_visible = True
            
