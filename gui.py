import asyncio
import logging
from time import perf_counter_ns

from database.requests import DataRequests
import flet as ft
from sqlalchemy.exc import SQLAlchemyError
from sort import sorts
from search import search


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
    search_menu = ft.Column(
        controls=[
            ft.TextButton("Linear Search", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLACK_54, color=ft.Colors.WHITE)),
            ft.TextButton("Binary Search", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLACK_54, color=ft.Colors.WHITE)),
        ],
        spacing=0,
        visible=False,
        scale=0.1,
        animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
    )
    sort_menu = ft.Column(
        controls=[
            ft.TextButton("Bubble Sort", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLACK_54, color=ft.Colors.WHITE)),
            ft.TextButton("Insertion Sort", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLACK_54, color=ft.Colors.WHITE)),
            ft.TextButton("Quick Sort", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLACK_54, color=ft.Colors.WHITE)),
            ft.TextButton("Pancake Sort", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLACK_54, color=ft.Colors.WHITE)),
        ],
        spacing=0,
        visible=False,
        scale=0.1,
        animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
    )
    lists = ft.ListView(
        controls=[ft.Text("No data to display")],
        align=ft.Alignment.CENTER,
        spacing=10,
        padding=20,
        width=700,
        height=200,
    )
    status = ft.Text()
    editing_data_id = None
    operation_results = {}
    selected_search = None
    saved_input_state = None

    def update_lists(data):
        if data:
            rows = []
            for item in data:
                async def edit_list(_, data_id=item.id, values=item.data):
                    nonlocal editing_data_id
                    editing_data_id = data_id
                    data_input.value = ", ".join(str(value) for value in values)
                    submit_button.content = "Update"
                    status.value = f"Editing list {data_id}."
                    page.update()

                async def delete_list(_, data_id=item.id):
                    nonlocal editing_data_id
                    try:
                        await DataRequests.delete_data(data_id)
                        operation_results.pop(data_id, None)
                        if editing_data_id == data_id:
                            editing_data_id = None
                            data_input.value = ""
                            submit_button.content = "Submit"
                        status.value = "List deleted."
                        await refresh_lists()
                    except SQLAlchemyError:
                        logging.exception("Failed to delete list %s", data_id)
                        status.value = "Could not delete the list. Check the application logs."
                        page.update()

                rows.append(
                    ft.Row(
                        controls=[
                            ft.Text(
                                operation_results.get(item.id, ""),
                                width=145,
                                size=12,
                            ),
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

    def restore_search_input():
        nonlocal selected_search, saved_input_state
        if saved_input_state is not None:
            data_input.value, data_input.hint_text, submit_button.content = saved_input_state
        selected_search = None
        saved_input_state = None

    async def refresh_lists():
        update_lists(await DataRequests.get_all_data())
        page.update()

    async def submit_search():
        nonlocal selected_search
        if not (data_input.value or "").strip():
            restore_search_input()
            status.value = "Search cancelled."
            page.update()
            return

        try:
            target = int(data_input.value.strip())
        except ValueError:
            status.value = "Enter an integer to search for."
            page.update()
            return

        algorithm_name, algorithm = selected_search
        submit_button.disabled = True
        search_button.disabled = True
        sort_button.disabled = True
        status.value = ""
        page.update()
        try:
            data = await DataRequests.get_all_data()
            operation_results.clear()
            if not data:
                status.value = "There are no lists to search."
            else:
                for item in data:
                    values = list(item.data)
                    search_values = (
                        list(dict.fromkeys(values))
                        if algorithm_name == "Binary Search"
                        else values
                    )
                    started = perf_counter_ns()
                    algorithm(search_values, target)
                    elapsed = (perf_counter_ns() - started) / 1_000_000_000
                    matches = values.count(target)
                    outcome = f"Found {matches}" if matches else "Not found"
                    operation_results[item.id] = f"{elapsed:.9f} s\n{outcome}"
                status.value = f"{algorithm_name} completed for all lists."
                await refresh_lists()
        except SQLAlchemyError:
            logging.exception("Failed to search saved lists")
            status.value = "Could not load the lists. Check the application logs."
        finally:
            restore_search_input()
            submit_button.disabled = False
            search_button.disabled = False
            sort_button.disabled = False
            page.update()

    async def apply_sort(algorithm_name, algorithm):
        restore_search_input()
        search_menu.visible = False
        search_menu.scale = 0.1
        sort_menu.visible = False
        sort_menu.scale = 0.1
        submit_button.disabled = True
        search_button.disabled = True
        sort_button.disabled = True
        status.value = ""
        page.update()
        try:
            data = await DataRequests.get_all_data()
            operation_results.clear()
            if not data:
                status.value = "There are no lists to sort."
            else:
                for item in data:
                    values = list(item.data)
                    started = perf_counter_ns()
                    sorted_values = algorithm(values)
                    elapsed = (perf_counter_ns() - started) / 1_000_000_000
                    if sorted_values is None:
                        sorted_values = values
                    await DataRequests.update_data(item.id, sorted_values)
                    operation_results[item.id] = f"{elapsed:.9f} s"
                status.value = f"{algorithm_name} completed for all lists."
                await refresh_lists()
        except SQLAlchemyError:
            logging.exception("Failed to sort saved lists")
            status.value = "Could not load or update the lists. Check the application logs."
        finally:
            submit_button.disabled = False
            search_button.disabled = False
            sort_button.disabled = False
            page.update()

    async def submit_data(_):
        nonlocal editing_data_id
        if selected_search is not None:
            await submit_search()
            return

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
            operation_results.clear()
            if editing_data_id is None:
                await DataRequests.create_data(values)
                status.value = "List saved."
            else:
                await DataRequests.update_data(editing_data_id, values)
                status.value = "List updated."
                editing_data_id = None
                submit_button.content = "Submit"
            await refresh_lists()
            data_input.value = ""
        except SQLAlchemyError:
            logging.exception("Failed to save or load lists")
            status.value = "Could not save the list. Check the application logs."
        finally:
            submit_button.disabled = False
            page.update()

    def choose_search(algorithm_name, algorithm):
        nonlocal selected_search, saved_input_state
        if selected_search is None:
            saved_input_state = (
                data_input.value,
                data_input.hint_text,
                submit_button.content,
            )
        selected_search = (algorithm_name, algorithm)
        data_input.value = ""
        data_input.hint_text = "Enter an integer to search for"
        submit_button.content = "Search"
        search_menu.visible = False
        search_menu.scale = 0.1
        sort_menu.visible = False
        sort_menu.scale = 0.1
        status.value = f"Selected {algorithm_name}. Enter a number and press Search."
        page.update()

    def make_sort_handler(algorithm_name, algorithm):
        async def select_sort(_):
            await apply_sort(algorithm_name, algorithm)

        return select_sort

    search_menu.controls[0].on_click = lambda _: choose_search("Linear Search", search.linear)
    search_menu.controls[1].on_click = lambda _: choose_search("Binary Search", search.binary)
    sort_menu.controls[0].on_click = make_sort_handler("Bubble Sort", sorts.Bubble_Sort)
    sort_menu.controls[1].on_click = make_sort_handler("Insertion Sort", sorts.insertion_sort)
    sort_menu.controls[2].on_click = make_sort_handler("Quick Sort", sorts.quicksort)
    sort_menu.controls[3].on_click = make_sort_handler("Pancake Sort", sorts.Pancake_sort)

    async def toggle_menu(menu, other_menu):
        if menu.visible:
            menu.visible = False
            menu.scale = 0.1
            page.update()
            return

        menu.visible = True
        menu.scale = 0.1
        other_menu.visible = False
        other_menu.scale = 0.1
        page.update()
        await asyncio.sleep(0.05)
        if menu.visible:
            menu.scale = 1
            page.update()

    async def toggle_search_menu(_):
        await toggle_menu(search_menu, sort_menu)

    async def toggle_sort_menu(_):
        await toggle_menu(sort_menu, search_menu)

    submit_button.on_click = submit_data
    search_button.on_click = toggle_search_menu
    sort_button.on_click = toggle_sort_menu

    stack = ft.Stack(
        controls=[
            background,
            ft.Column(
                controls=[
                    ft.Row(controls=[text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[lists], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[data_input, submit_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[status], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(
                        controls=[search_menu, search_button, sort_button, sort_menu],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
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