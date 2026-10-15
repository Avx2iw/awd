import flet as ft
import math
 
def main(page: ft.Page):
    page.title = "Searching and Sorting Algorithms"
    page.padding = 0
    text = ft.Text("Searching and Sorting Algorithms", size=30, data=0, font_family="Copperplate Gothic")
    data_input = ft.TextField(hint_text="Enter your data", expand=True)
    background = ft.Container(gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=["#F1EDEC", "#696969", "#424242"]), width=page.width, height=page.height)
 
    stack = ft.Stack(
        controls=[
            background,
            ft.Column(
                controls=[
                    ft.Row(controls=[text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[data_input]),
                    ft.Row(controls=[ft.Button("Search", margin=10), ft.Button("Sort", margin=10)]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        width=page.width,
        height=page.height,
    )
 
    page.add(stack)
 
ft.run(main)