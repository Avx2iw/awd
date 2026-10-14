from search import search
from sort import sorts
import flet as ft

def main(page: ft.Page):
    page.title = "Searching and Sorting Algorithms"
    text = ft.Text("Searching and Sorting Algorithms", size=30, data=0, font_family="Copperplate Gothic")
    data_input = ft.TextField(hint_text="Enter your data", expand=True)

    page.add(
        ft.Row(controls=[text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[data_input])
    )

ft.run(main)