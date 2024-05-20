import flet
from flet import Page, CrossAxisAlignment, MainAxisAlignment
from importes import (
    Pagina_tiendas,
    Pagina_empleados,
    Inicio,
    First_page,
)


ANCHO_PAGINA = 1680
ALTO_PAGINA = 900


def main(page: Page):
    page.title = "El mercado de Marcos"

    page.window_width = ANCHO_PAGINA
    page.window_height = ALTO_PAGINA
    page.padding = 0
    page.window_resizable = False
    page.window_maximizable = False

    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER

    def router(route):
        page.views.clear()

        if page.route == "/inicio":
            Pagina_inicio = Inicio(page)
            page.views.append(Pagina_inicio)
        elif page.route == "/primera":
            Pagina_primera = First_page(page)
            page.views.append(Pagina_primera)
        elif page.route == "/tiendas":
            Objeto_pagina_tiendas = Pagina_tiendas(page)
            page.views.append(Objeto_pagina_tiendas)
        elif page.route == "/empleados":
            Objeto_pagina_empleados = Pagina_empleados(page)
            page.views.append(Objeto_pagina_empleados)

        page.update()

    page.on_route_change = router
    page.go("/inicio")


if __name__ == "__main__":
    flet.app(target=main)
