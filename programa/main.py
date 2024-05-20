import flet
from flet import *
from importes import (
    Inicio,
    boton_menu,
    First_page,
    Pagina_tiendas,
    Pagina_empleados,
)


ANCHO_PAGINA = 1680
ALTO_PAGINA = 900


def main(page: Page):
    page.title = "El mercado de Marcos"
    page.bgcolor = "#1f2f2f"

    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window_width = ANCHO_PAGINA
    page.window_height = ALTO_PAGINA
    page.padding = 0
    page.window_resizable = False
    page.window_maximizable = False

    def cambiar_pagina(e) -> None:
        page.controls.clear()
        index = e.control.selected_index
        if index == 0:
            page.add(primera_pagina)
        elif index == 1:
            page.add(pagina_tiendas)
        elif index == 2:
            page.add(pagina_empleados)
        page.update()

    page.drawer = NavigationDrawer(
        on_change=cambiar_pagina,
        controls=[
            Container(height=12),
            NavigationDrawerDestination(
                label="Inicio",
                icon=icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=Icon(icons.DOOR_BACK_DOOR),
            ),
            Container(height=12),
            Container(height=2, bgcolor=colors.BLACK),
            Container(height=12),
            NavigationDrawerDestination(
                label="Añadir Tienda",
                icon=icons.SHOP_2_OUTLINED,
                selected_icon_content=Icon(icons.SHOP_2),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Añadir Empleado",
                icon=icons.PERSON_OUTLINED,
                selected_icon_content=Icon(icons.PERSON),
            ),
        ],
    )

    def show_drawer(e) -> None:
        page.drawer.open = True
        page.drawer.update()

    def cambiar_vista_principal():
        page.add(primera_pagina)

    boton_drawer = boton_menu(show_drawer)

    pagina_inicio = Inicio(page, cambiar_vista_principal)
    primera_pagina = First_page(boton_drawer, page)
    pagina_tiendas = Pagina_tiendas(boton_drawer, page)
    pagina_empleados = Pagina_empleados(boton_drawer, page)

    page.add(pagina_inicio)
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
