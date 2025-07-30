import flet as ft
from importlib import resources

def get_image_path():
    return str(resources.files("quantum_platform.assets").joinpath("量子力学界面图.jpg"))

IMAGE_PATH = get_image_path()

def main(page: ft.Page):
    page.title = "量子力学教学平台"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False
    page.bgcolor = "white"  # Updated: no ft.colors

    page.controls.append(
        ft.Image(src=IMAGE_PATH, width=800, height=600, fit=ft.ImageFit.COVER)
    )

    page.update()

if __name__ == '__main__':
    ft.app(target=main)
