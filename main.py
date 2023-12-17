import flet as ft
from whisper_app import WhisperApp


def main(page: ft.Page):
    page.title="Whisper UI Demo"
    WhisperApp(page)
    
ft.app(target=main)

