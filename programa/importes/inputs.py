from flet import *
from importes.bdd import (
    sacar_informacion,
    connect_to_database,
    insert_in_tiendas,
    insert_in_jefes,
    select_sencillo,
)


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
            pass
        else:
            self.input_filter = NumbersOnlyInputFilter()


class Tabla(DataTable):
    def __init__(self) -> None:
        super().__init__()
        self.columns = [
            DataColumn(Text("DNI")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Apellidos")),
            DataColumn(Text("Tiendas")),
        ]
        db = connect_to_database()
        filas = select_sencillo(db, "jefes", "DNI_jefe, nombre, apellidos, tiendas")
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(i[0])),
                        DataCell(Text(i[1])),
                        DataCell(Text(i[2])),
                        (
                            DataCell(Text(i[3]))
                            if i[3] is not None
                            else DataCell(Text("Sin Tiendas"))
                        ),
                    ]
                )
            )
        self.width = 700
        self.bgcolor = colors.GREY_100
        self.border_radius = 20
        self.heading_text_style = TextStyle(weight=FontWeight.BOLD)

    def fill_data(self):
        db = connect_to_database()
        filas = select_sencillo(db, "jefes", "DNI_jefe, nombre, apellidos, tiendas")
        db.close()
        self.rows = []
        for i in filas:
            self.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(i[0])),
                        DataCell(Text(i[1])),
                        DataCell(Text(i[2])),
                        (
                            DataCell(Text(i[3]))
                            if i[3] is not None
                            else DataCell(Text("Sin Tiendas"))
                        ),
                    ]
                )
            )
        self.update()


class InputTienda(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.tienda = Casilla_de_informacion("Tienda", "Nombre de la tienda", "str")
        self.jefe = Casilla_de_informacion("Jefe", "DNI del jefe", "str")
        self.n_local = Casilla_de_informacion(
            "Local", "Local en el que quiere abrir la tienda", "int"
        )
        self.informador = Text()
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.controls = [
            Text("Tiendas", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.tienda,
            Divider(height=10),
            self.jefe,
            Divider(height=10),
            self.n_local,
            Divider(height=10),
            TextButton("Añadir tienda", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]
        self.funcion = funcion

    def cambiar_rojo(self, TextField, text) -> bool:
        if TextField.value != "":
            TextField.label = text
            TextField.label_style = TextStyle(color=colors.BLACK)
            return True

        TextField.label = text + " es obligatorio *"
        TextField.label_style = TextStyle(color=colors.RED)

        return False

    def add_clicked(self, e) -> None:
        operacion = self.cambiar_rojo(self.tienda, "Tienda")
        operacion = self.cambiar_rojo(self.jefe, "Jefe") and operacion
        operacion = self.cambiar_rojo(self.n_local, "Local") and operacion

        if operacion:
            db = connect_to_database()

            if (
                len(
                    sacar_informacion(
                        db, "tiendas", "nombre", "nombre", (self.tienda.value.upper())
                    )
                )
                > 0
            ):
                db.close()
                self.informador.color = colors.RED
                self.informador.value = (
                    "Esa tienda ya existe, ingresa otro nombre distinto"
                )
            elif (
                len(
                    sacar_informacion(
                        db, "jefes", "DNI_jefe", "DNI_jefe", (self.jefe.value)
                    )
                )
                == 0
            ):
                db.close()
                self.informador.color = colors.RED
                self.informador.value = (
                    "El jefe que intenta usar no existe en la base de datos"
                )

            elif (
                len(
                    sacar_informacion(
                        db, "tiendas", "nombre", "jefe", (self.jefe.value)
                    )
                )
                > 2
            ):
                db.close()
                self.informador.color = colors.RED
                self.informador.value = "El Jefe que intenta usar ya tiene 3 tiendas"
            elif (
                len(
                    sacar_informacion(
                        db, "tiendas", "n_local", "n_local", (self.n_local.value)
                    )
                )
                > 0
            ):
                db.close()
                self.informador.color = colors.RED
                self.informador.value = "Ese local ya está en uso"

            else:
                insert_in_tiendas(
                    db, (self.tienda.value.upper(), self.jefe.value, self.n_local.value)
                )

                db.close()
                self.funcion()

                self.tienda.value = ""
                self.jefe.value = ""
                self.n_local.value = ""
                self.informador.color = colors.GREEN
                self.informador.value = "Tienda añadida con exito"
        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.tienda.update()
        self.jefe.update()
        self.n_local.update()
        self.informador.update()


class InputJefe(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.dni_jefe = Casilla_de_informacion(
            "DNI", "Documento Nacional de Identidad", "str"
        )
        self.nombre = Casilla_de_informacion("Nombre", "Nombre del jefe", "str")
        self.apellidos = Casilla_de_informacion(
            "Apellidos", "Apellidos del jefe", "str"
        )
        self.telefono = Casilla_de_informacion("Telefono", "Telefono del jefe", "str")
        self.domicilio = Casilla_de_informacion(
            "Domicilio", "Direccion del hogar", "str"
        )
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.informador = Text()
        self.controls = [
            Text("Dueños", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.dni_jefe,
            Divider(height=10),
            self.nombre,
            Divider(height=10),
            self.apellidos,
            Divider(height=10),
            self.telefono,
            Divider(height=10),
            self.domicilio,
            Divider(height=10),
            TextButton("Añadir dueño", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]
        self.funcion = funcion

    def cambiar_rojo(self, TextField, text) -> bool:
        if TextField.value != "":
            TextField.label = text
            TextField.label_style = TextStyle(color=colors.BLACK)
            return True

        TextField.label = text + " es obligatorio *"
        TextField.label_style = TextStyle(color=colors.RED)

        return False

    def add_clicked(self, e) -> None:
        operacion = self.cambiar_rojo(self.dni_jefe, "DNI")
        operacion = self.cambiar_rojo(self.nombre, "Nombre") and operacion
        operacion = self.cambiar_rojo(self.apellidos, "Apellidos") and operacion
        operacion = self.cambiar_rojo(self.telefono, "Telefono") and operacion
        operacion = self.cambiar_rojo(self.domicilio, "Domicilio") and operacion

        if operacion:
            db = connect_to_database()

            if (
                len(
                    sacar_informacion(
                        db,
                        "jefes",
                        "DNI_jefe",
                        "DNI_jefe",
                        (self.dni_jefe.value.upper()),
                    )
                )
                > 0
            ):
                db.close()
                self.informador.color = colors.RED
                self.informador.value = "Ya existe un Dueño con ese DNI"
            elif len(self.dni_jefe.value) != 9:
                db.close()
                self.informador.color = colors.RED
                self.informador.value = "El DNI no tiene la longitud correcta"

            else:
                insert_in_jefes(
                    db,
                    (
                        self.dni_jefe.value.upper(),
                        self.nombre.value,
                        self.apellidos.value,
                        self.telefono.value,
                        self.domicilio.value,
                    ),
                )

                db.close()
                self.funcion()

                self.dni_jefe.value = ""
                self.nombre.value = ""
                self.apellidos.value = ""
                self.telefono.value = ""
                self.domicilio.value = ""
                self.informador.color = colors.GREEN
                self.informador.value = "Duelo añadido con exito"
        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.dni_jefe.update()
        self.nombre.update()
        self.apellidos.update()
        self.telefono.update()
        self.domicilio.update()
        self.informador.update()
