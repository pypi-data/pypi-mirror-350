import flet as ft
from importlib import resources
from pathlib import Path

def get_image_path():
    with resources.path("quantum_platform.assets", "量子力学界面图.jpg") as p:
        return str(p)

IMAGE_PATH = get_image_path()

def main(page: ft.Page):
    page.title = "量子力学教学平台"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False
    page.bgcolor = ft.colors.WHITE

    page.controls.append(
        ft.Image(src=IMAGE_PATH, width=800, height=600, fit=ft.ImageFit.COVER)
    )

    page.update()

if __name__ == '__main__':
    ft.app(target=main)
