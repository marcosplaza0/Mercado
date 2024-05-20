import flet
from flet import *


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
        ]

    def cambiar_pagina(self, e):
        index = e.control.selected_index
        if index == 0:
            self.view.page.go("/primera")
        elif index == 1:
            self.view.page.go("/tiendas")
        elif index == 2:
            self.view.page.go("/empleados")

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


class Header(Row):
    def __init__(self, titulo, function):
        super().__init__()
        self.alignment = MainAxisAlignment.SPACE_BETWEEN
        self.vertical_alignment = CrossAxisAlignment.CENTER
        self.controls = [
            IconButton(
                icons.MENU,
                on_click=lambda e: function(e),
            ),
            Text(
                titulo,
                color=colors.BLACK,
                size=30,
                weight=FontWeight.BOLD,
            ),
            Divider(),
        ]


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
                        Divider(height=1),
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
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Añadir Empleados", self.drawer.show_drawer),
                        Divider(height=1),
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
        self.controls = [
            Container(
                bgcolor=colors.WHITE,
                margin=0,
                height=self.page.height,
                content=Column(
                    controls=[
                        Header("Añadir Tiendas", self.drawer.show_drawer),
                        Divider(height=1),
                    ],
                ),
            )
        ]


class Casilla_de_informacion(TextField):
    def __init__(self, titulo, hint, tipo) -> None:
        super().__init__()
        self.label = titulo
        self.border = InputBorder.UNDERLINE
        self.filled = True
        self.hint_text = hint
        self.hint_style = TextStyle(color=colors.BLACK54)
        self.bgcolor = colors.BLACK12
        self.color = colors.BLACK
        self.label_style = TextStyle(color=colors.BLACK)
        if tipo == "str":
            self.input_filter = TextOnlyInputFilter()
            self.keyboard_type = KeyboardType.TEXT
        else:
            self.input_filter = NumbersOnlyInputFilter()
            self.keyboard_type = KeyboardType.NUMBER


class InputTienda(Column):
    def __init__(self) -> None:
        super().__init__()
        self.informador = Text()

    def build(self):
        return Container(
            padding=padding.only(left=30, right=30),
            content=Column(
                controls=[
                    self.glucemia_inicial,
                    self.glucemia_final,
                    self.raciones,
                    self.unidades,
                    TextButton(
                        "Añadir nota", icon=icons.ADD, on_click=self.add_clicked
                    ),
                    self.informador,
                ]
            ),
        )

    def cambiar_rojo(self, TextField, text) -> bool:
        if TextField.nota.value != "":
            TextField.nota.label = text
            TextField.nota.label_style = TextStyle(color=colors.BLACK)
            return True

        TextField.nota.label = text + " es obligatorio *"
        TextField.nota.label_style = TextStyle(color=colors.RED)

        return False

    def add_clicked(self, e) -> None:
        operacion = self.cambiar_rojo(self.glucemia_inicial, "Glucemia Inicial")
        operacion = self.cambiar_rojo(self.raciones, "Comida") and operacion
        operacion = self.cambiar_rojo(self.unidades, "Insulina") and operacion

        if operacion:
            Fecha = datetime.now().strftime("%b %d, %Y %I:%M")
            db = Database.ConnectToDatabase()
            if self.glucemia_final.nota.value == "":
                Database.InsertDatabase(
                    db,
                    (
                        Fecha,
                        float(self.glucemia_inicial.nota.value),
                        None,
                        float(self.raciones.nota.value),
                        float(self.unidades.nota.value),
                        None,
                    ),
                )
            else:
                resultado = calculo(
                    self.glucemia_inicial.nota.value,
                    self.raciones.nota.value,
                    self.unidades.nota.value,
                    self.glucemia_final.nota.value,
                )
                Database.InsertDatabase(
                    db,
                    (
                        Fecha,
                        float(self.glucemia_inicial.nota.value),
                        float(self.glucemia_final.nota.value),
                        float(self.raciones.nota.value),
                        float(self.unidades.nota.value),
                        resultado,
                    ),
                )

            db.close()

            self.glucemia_inicial.nota.value = ""
            self.raciones.nota.value = ""
            self.unidades.nota.value = ""
            self.glucemia_final.nota.value = ""
            self.informador.color = colors.GREEN
            self.informador.value = " Nota añadida con exito"
        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.glucemia_inicial.update()
        self.glucemia_final.update()
        self.raciones.update()
        self.unidades.update()
        self.informador.update()
