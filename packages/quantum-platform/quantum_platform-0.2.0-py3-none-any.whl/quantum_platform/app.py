import flet as ft
from quantum_platform.main_page import MainPage

def main(page: ft.Page):
    app = MainPage(page)
    app.build()

if __name__ == "__main__":
    ft.app(target=main)
