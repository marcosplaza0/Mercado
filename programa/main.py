import flet
from flet import Page, CrossAxisAlignment, MainAxisAlignment
from importes import (
    Pagina_tiendas,
    Pagina_empleados,
    Pagina_productos,
    Pagina_pedidos,
    Pagina_compras,
    Pagina_busqueda,
    Pagina_deletes,
    Inicio,
    First_page,
    init_database,
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
        elif page.route == "/productos":
            Objeto_pagina_productos = Pagina_productos(page)
            page.views.append(Objeto_pagina_productos)
        elif page.route == "/pedidos":
            Objeto_pagina_pedidos = Pagina_pedidos(page)
            page.views.append(Objeto_pagina_pedidos)
        elif page.route == "/compras":
            Objeto_pagina_compras = Pagina_compras(page)
            page.views.append(Objeto_pagina_compras)
        elif page.route == "/busqueda":
            Objeto_pagina_busqueda = Pagina_busqueda(page)
            page.views.append(Objeto_pagina_busqueda)
        elif page.route == "/basura":
            Objeto_pagina_borrador = Pagina_deletes(page)
            page.views.append(Objeto_pagina_borrador)

        page.update()

    page.on_route_change = router
    page.go("/inicio")


if __name__ == "__main__":
    init_database()
    flet.app(target=main)
