import flet
from flet import *


ANCHO_PAGINA = 1680
ALTO_PAGINA = 900

Bienvenida = Stack(
    [
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
    ]
)


class Inicio(Column):
    def __init__(self, page: Page, funcion):
        super().__init__()
        self.pg: Page = page
        self.funcion = funcion

    def button_clicked(self, e):
        self.pg.controls.pop(-1)
        self.funcion()
        self.pg.update()

    def build(self):
        carta = Card(
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
                                Bienvenida,
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
                            on_click=self.button_clicked,
                        ),
                    ],
                ),
            ),
        )
        return carta


class boton_menu(IconButton):
    def __init__(self, show_drawer):
        super().__init__()
        self.icon = icons.MENU
        self.on_click = show_drawer


class Pagina_tiendas(Column):
    def __init__(self, boton_dr, pg):
        super().__init__()
        self.boton = boton_dr
        self.page = pg

    def build(self):
        pagina = Container(
            bgcolor=colors.WHITE,
            margin=0,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            height=self.page.height,
            content=Column(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.boton,
                            Text(
                                "Añadir Tiendas",
                                color=colors.BLACK,
                                size=30,
                                weight=FontWeight.BOLD,
                            ),
                            Divider(),
                        ],
                    ),
                    Divider(height=1),
                ],
            ),
        )
        return pagina


class First_page(Column):
    def __init__(self, boton_dr, pg):
        super().__init__()
        self.boton = boton_dr
        self.page = pg

    def build(self):
        pagina = Container(
            bgcolor=colors.WHITE,
            margin=0,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            height=self.page.height,
            content=Column(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.boton,
                            Text(
                                "Inicio",
                                color=colors.BLACK,
                                size=30,
                                weight=FontWeight.BOLD,
                            ),
                            Divider(),
                        ],
                    ),
                    Divider(height=1),
                ],
            ),
        )
        return pagina


class Pagina_empleados(Column):
    def __init__(self, boton_dr, pg):
        super().__init__()
        self.boton = boton_dr
        self.page = pg

    def build(self):
        pagina = Container(
            bgcolor=colors.WHITE,
            margin=0,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            height=self.page.height,
            content=Column(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.boton,
                            Text(
                                "Añadir Empleados",
                                color=colors.BLACK,
                                size=30,
                                weight=FontWeight.BOLD,
                            ),
                            Divider(),
                        ],
                    ),
                    Divider(height=1),
                ],
            ),
        )
        return pagina
