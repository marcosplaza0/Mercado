import flet
from flet import *
from importes.inputs import (
    InputTienda,
    InputJefe,
    InputEmpleado,
    InputProductos,
    InputPedidos,
    InputCompras,
    InputBusqueda,
)
from importes.displays_info import Tabla, TablaAvanzada


ANCHO_PAGINA = 1680
ALTO_PAGINA = 900


class Menu_drawer(NavigationDrawer):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.on_change = lambda e: self.cambiar_pagina(e)
        self.controls = [
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
                label="Añadir tiendas",
                icon=icons.SHOP_TWO_OUTLINED,
                selected_icon_content=Icon(icons.SHOP_TWO),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Añadir empleados",
                icon=icons.PERSON_OUTLINED,
                selected_icon_content=Icon(icons.PERSON),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Añadir productos",
                icon=icons.FOOD_BANK_OUTLINED,
                selected_icon_content=Icon(icons.FOOD_BANK),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Añadir stock",
                icon=icons.PLUS_ONE_OUTLINED,
                selected_icon_content=Icon(icons.PLUS_ONE),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Hacer pedidos",
                icon=icons.SHOPIFY_OUTLINED,
                selected_icon_content=Icon(icons.SHOPIFY),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Buscar Información",
                icon=icons.LENS_OUTLINED,
                selected_icon_content=Icon(icons.LENS),
            ),
            Container(height=12),
            NavigationDrawerDestination(
                label="Eliminador",
                icon=icons.BLOCK_OUTLINED,
                selected_icon_content=Icon(icons.BLOCK),
            ),
        ]

    def cambiar_pagina(self, e):
        index = e.control.selected_index
        if index == 0:
            self.view.page.go("/primera")
        elif index == 1:
            self.view.page.go("/tiendas")
        elif index == 2:
            self.view.page.go("/empleados")
        elif index == 3:
            self.view.page.go("/productos")
        elif index == 4:
            self.view.page.go("/compras")
        elif index == 5:
            self.view.page.go("/pedidos")
        elif index == 6:
            self.view.page.go("/busqueda")
        elif index == 7:
            self.view.page.go("/basura")

    def show_drawer(self, e):
        self.view.drawer.open = True
        self.view.update()


class Inicio(View):
    def __init__(self, page: Page):
        super(Inicio, self).__init__(
            route="/inicio",
            bgcolor="#1f2f2f",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.pg: Page = page
        self.controls = [
            Card(
                width=ANCHO_PAGINA * 0.7,
                height=ALTO_PAGINA * 0.8,
                elevation=30,
                content=Container(
                    border_radius=10,
                    margin=30,
                    padding=30,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            Column(
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Text(
                                        spans=[
                                            TextSpan(
                                                "Mercados Marcos",
                                                TextStyle(
                                                    size=80,
                                                    weight=FontWeight.BOLD,
                                                    color=colors.BLACK,
                                                ),
                                            ),
                                        ],
                                    ),
                                    Divider(
                                        color=colors.BLACK,
                                        height=3,
                                    ),
                                ],
                            ),
                            Text(
                                "Para comprar de forma inteligente, ve a un lugar inteligente",
                                size=20,
                            ),
                            ElevatedButton(
                                "Comencemos",
                                icon=icons.PLAYLIST_PLAY_OUTLINED,
                                on_click=lambda e: self.pg.go("/primera"),
                            ),
                        ],
                    ),
                ),
            )
        ]


class Header(Container):
    def __init__(self, titulo, function):
        super().__init__()
        self.vertical_alignment = CrossAxisAlignment.CENTER
        self.padding = padding.only(top=10, bottom=12)
        self.margin = margin.only(bottom=10)
        self.bgcolor = colors.GREY_200
        self.shadow = BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=colors.BLUE_GREY_300,
            offset=Offset(0, 0),
            blur_style=ShadowBlurStyle.OUTER,
        )
        self.content = Row(
            [
                Container(width=12),
                IconButton(
                    icons.MENU,
                    on_click=lambda e: function(e),
                ),
                Text(
                    "  " + titulo,
                    color=colors.BLACK,
                    size=30,
                    weight=FontWeight.BOLD,
                ),
            ]
        )


class First_page(View):
    def __init__(self, pg):
        super(First_page, self).__init__(
            route="/primera",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Inicio", self.drawer.show_drawer),
                    ],
                ),
            )
        ]


class Pagina_tiendas(View):
    def __init__(self, pg):
        super(Pagina_tiendas, self).__init__(
            route="/tiendas",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = Tabla(
            ("DNI", "Nombre", "Apellidos", "Tiendas"),
            "jefes",
            "DNI_jefe, nombre, apellidos, tiendas",
        )
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Añadir Tiendas", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Row(
                                    controls=[
                                        Card(
                                            elevation=25,
                                            content=Container(
                                                margin=margin.only(top=30),
                                                padding=padding.only(
                                                    top=30, left=20, right=20, bottom=20
                                                ),
                                                border_radius=10,
                                                content=InputJefe(
                                                    self.tablon.fill_data
                                                ),
                                            ),
                                        ),
                                        Container(width=20),
                                        Card(
                                            elevation=25,
                                            content=Container(
                                                margin=margin.only(top=30),
                                                padding=padding.only(
                                                    top=40, left=20, right=20, bottom=30
                                                ),
                                                border_radius=10,
                                                content=InputTienda(
                                                    self.tablon.fill_data
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                Column(
                                    height=650,
                                    scroll=ScrollMode.ALWAYS,
                                    controls=[
                                        self.tablon,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]


class Pagina_empleados(View):
    def __init__(self, pg):
        super(Pagina_empleados, self).__init__(
            route="/empleados",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = Tabla(
            ("DNI", "Nombre", "Apellidos", "Jefe", "Tiendas"),
            "empleados",
            "DNI_empleados, nombre, apellidos, dni_jefe, tiendas",
        )
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Añadir Empleados", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Card(
                                    elevation=25,
                                    content=Container(
                                        margin=margin.only(top=30),
                                        padding=padding.only(
                                            top=40, left=20, right=20, bottom=30
                                        ),
                                        border_radius=10,
                                        content=InputEmpleado(self.tablon.fill_data),
                                    ),
                                ),
                                Column(
                                    height=650,
                                    scroll=ScrollMode.ALWAYS,
                                    controls=[
                                        self.tablon,
                                    ],
                                ),
                            ],
                        ),
                        Text(
                            "                   Para ingresar un"
                            " empleado ya existente, solo hace falta"
                            " que rellene\n                   los"
                            " campos de DNI, Tienda, Tipo de Jornada y Sueldo",
                            size=20,
                        ),
                    ],
                ),
            )
        ]


class Pagina_productos(View):
    def __init__(self, pg):
        super(Pagina_productos, self).__init__(
            route="/productos",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = Tabla(
            ("Nombre", "Tipo", "Cantidad", "Tiendas", "Precio_c", "Precio_v"),
            "productos",
            "Nombre, Tipo, Cantidad, Tienda, Precio_compra, Precio_venta",
        )
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Añadir Productos", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Card(
                                    elevation=25,
                                    content=Container(
                                        margin=margin.only(top=30),
                                        padding=padding.only(
                                            top=40, left=20, right=20, bottom=30
                                        ),
                                        border_radius=10,
                                        content=InputProductos(self.tablon.fill_data),
                                    ),
                                ),
                                Column(
                                    height=650,
                                    scroll=ScrollMode.ALWAYS,
                                    controls=[
                                        self.tablon,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]


class Pagina_pedidos(View):
    def __init__(self, pg):
        super(Pagina_pedidos, self).__init__(
            route="/pedidos",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = Tabla(
            ("Nombre", "Tienda", "Cantidad", "Coste (€)", "Fecha"),
            "pedidos",
            "producto, tienda, cantidad, recibos, Fecha",
        )
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Pedidos", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Card(
                                    elevation=25,
                                    content=Container(
                                        margin=margin.only(top=30),
                                        padding=padding.only(
                                            top=40, left=20, right=20, bottom=30
                                        ),
                                        border_radius=10,
                                        content=InputPedidos(self.tablon.fill_data),
                                    ),
                                ),
                                Column(
                                    height=650,
                                    scroll=ScrollMode.ALWAYS,
                                    controls=[
                                        self.tablon,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]


class Pagina_compras(View):
    def __init__(self, pg):
        super(Pagina_compras, self).__init__(
            route="/compras",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = Tabla(
            ("Nombre", "Tienda", "Cantidad", "Importe (€)", "Fecha"),
            "compras",
            "producto, tienda, cantidad, pago, Fecha",
        )
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Añadir stock", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Card(
                                    elevation=25,
                                    content=Container(
                                        margin=margin.only(top=30),
                                        padding=padding.only(
                                            top=40, left=20, right=20, bottom=30
                                        ),
                                        border_radius=10,
                                        content=InputCompras(self.tablon.fill_data),
                                    ),
                                ),
                                Column(
                                    height=650,
                                    scroll=ScrollMode.ALWAYS,
                                    controls=[
                                        self.tablon,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]


class Pagina_busqueda(View):
    def __init__(self, pg):
        super(Pagina_busqueda, self).__init__(
            route="/busqueda",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = TablaAvanzada()
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Busqueda personalizada", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Card(
                                    elevation=25,
                                    content=Container(
                                        margin=margin.only(top=30),
                                        padding=padding.only(
                                            top=40, left=20, right=20, bottom=30
                                        ),
                                        border_radius=10,
                                        content=InputBusqueda(self.tablon),
                                    ),
                                ),
                                Column(
                                    height=650,
                                    scroll=ScrollMode.ALWAYS,
                                    controls=[
                                        self.tablon,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]


class Pagina_deletes(View):
    def __init__(self, pg):
        super(Pagina_deletes, self).__init__(
            route="/basura",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            padding=0,
        )
        self.drawer: NavigationDrawer = Menu_drawer(self)
        self.page = pg
        self.tablon = TablaAvanzada()
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Borrar objetos", self.drawer.show_drawer),
                        Row(
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                Card(
                                    elevation=25,
                                    content=Container(
                                        margin=margin.only(top=30),
                                        padding=padding.only(
                                            top=40, left=20, right=20, bottom=30
                                        ),
                                        border_radius=10,
                                        content=InputBusqueda(self.tablon),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]
