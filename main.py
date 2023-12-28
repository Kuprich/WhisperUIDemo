import flet as ft
from whisper_ui.whisper_app import WhisperApp


def main(page: ft.Page):
    page.title="Whisper UI v2.0"
    app = WhisperApp(page)
    page.add(app)
    
ft.app(target=main)


