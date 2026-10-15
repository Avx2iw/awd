import logging

from database.requests import DataRequests
import flet as ft
from sqlalchemy.exc import SQLAlchemyError
from awd.sort import sorts
from awd.search import search


async def main(page: ft.Page):
    await DataRequests.initialize_database()

    page.title = "Searching and Sorting Algorithms"
    page.padding = 0
    text = ft.Text("Searching and Sorting Algorithms", size=30, font_family="Copperplate Gothic")
    data_input = ft.TextField(hint_text="Enter your data", width=300, height=50, text_align=ft.TextAlign.CENTER, border_color="#696969", border_radius=10, border_width=2)
    submit_button = ft.Button("Submit", icon=ft.Icons.CHECK, color=ft.Colors.WHITE, icon_color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
    background = ft.Container(gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=["#F1EDEC", "#696969", "#424242"]), width=page.width, height=page.height)
    search_button = ft.Button("Search", icon=ft.Icons.SEARCH, color=ft.Colors.WHITE, icon_color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
    sort_button = ft.Button("Sort", icon=ft.Icons.SORT, color=ft.Colors.WHITE, icon_color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
    lists = ft.ListView(
        controls=[ft.Text("No data to display")],
        align=ft.Alignment.CENTER,
        spacing=10,
        padding=20,
        width=400,
        height=200,
    )
    status = ft.Text()
    editing_data_id = None

    def update_lists(data):
        if data:
            rows = []
            for item in data:
                async def edit_list(_, data_id=item.id, values=item.data):
                    nonlocal editing_data_id
                    editing_data_id = data_id
                    data_input.value = ", ".join(str(value) for value in values)
                    submit_button.text = "Update"
                    status.value = f"Editing list {data_id}."
                    page.update()

                async def delete_list(_, data_id=item.id):
                    nonlocal editing_data_id
                    try:
                        await DataRequests.delete_data(data_id)
                        if editing_data_id == data_id:
                            editing_data_id = None
                            data_input.value = ""
                            submit_button.text = "Submit"
                        status.value = "List deleted."
                        await refresh_lists()
                    except SQLAlchemyError:
                        logging.exception("Failed to delete list %s", data_id)
                        status.value = "Could not delete the list. Check the application logs."
                        page.update()

                rows.append(
                    ft.Row(
                        controls=[
                            ft.Text(str(item.data), expand=True),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Edit list",
                                on_click=edit_list,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Delete list",
                                on_click=delete_list,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
            lists.controls = rows
        else:
            lists.controls = [ft.Text("No data to display")]

    async def refresh_lists():
        update_lists(await DataRequests.get_all_data())
        page.update()

    async def submit_data(_):
        nonlocal editing_data_id
        try:
            values = [
                int(value)
                for value in (data_input.value or "").replace(",", " ").split()
            ]
        except ValueError:
            status.value = "Enter integers separated by spaces or commas."
            page.update()
            return

        if not values:
            status.value = "Enter at least one integer."
            page.update()
            return

        submit_button.disabled = True
        status.value = ""
        page.update()
        try:
            if editing_data_id is None:
                await DataRequests.create_data(values)
                status.value = "List saved."
            else:
                await DataRequests.update_data(editing_data_id, values)
                status.value = "List updated."
                editing_data_id = None
                submit_button.text = "Submit"
            await refresh_lists()
            data_input.value = ""
        except SQLAlchemyError:
            logging.exception("Failed to save or load lists")
            status.value = "Could not save the list. Check the application logs."
        finally:
            submit_button.disabled = False
            page.update()

    submit_button.on_click = submit_data

    stack = ft.Stack(
        controls=[
            background,
            ft.Column(
                controls=[
                    ft.Row(controls=[text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[lists], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[data_input, submit_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[status], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[search_button, sort_button], alignment=ft.MainAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        width=page.width,
        height=page.height,
    )
 
    page.add(stack)
    await refresh_lists()
 
ft.run(main)