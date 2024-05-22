from flet import (
    DataTable,
    DataColumn,
    DataCell,
    DataRow,
    Text,
    colors,
    FontWeight,
    TextStyle,
)
from importes.bdd import connect_to_database, select_sencillo


class Tabla(DataTable):
    def __init__(self, header: tuple, tabla, campos) -> None:
        super().__init__()
        self.tabla = tabla
        self.campos = campos
        for i in header:
            self.columns.append(DataColumn(Text(i)))

        db = connect_to_database()
        filas = select_sencillo(db, self.tabla, self.campos)
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )

        self.width = 700
        self.bgcolor = colors.GREY_100
        self.border_radius = 20
        self.heading_text_style = TextStyle(weight=FontWeight.BOLD)

    def fill_data(self):
        db = connect_to_database()
        filas = select_sencillo(db, self.tabla, self.campos)
        db.close()
        self.rows = []
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )
        self.update()


class TablaAvanzada(DataTable):
    def __init__(self) -> None:
        super().__init__()
        self.columns = [
            DataColumn(Text("Nombre")),
            DataColumn(Text("Jefe")),
            DataColumn(Text("N_local")),
            DataColumn(Text("T_productos")),
            DataColumn(Text("N_empleados")),
            DataColumn(Text("Empleados")),
        ]

        db = connect_to_database()
        c = db.cursor()
        c.execute("SELECT * FROM tiendas")
        filas = c.fetchall()
        c.close()
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )

        self.width = 1000
        self.bgcolor = colors.GREY_100
        self.border_radius = 20
        self.heading_text_style = TextStyle(weight=FontWeight.BOLD)

    def productos_por_tienda_s(self, tienda):
        self.columns = [
            DataColumn(Text("Nombre")),
            DataColumn(Text("Tipo")),
            DataColumn(Text("Cantidad")),
            DataColumn(Text("Tienda")),
            DataColumn(Text("Precio_C")),
            DataColumn(Text("Precio_V")),
        ]
        self.rows = []
        self.width = 1000
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT * FROM productos WHERE Tienda == '{tienda}' ")
        filas = c.fetchall()
        c.close()
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )
        self.update()

    def empleados_por_tienda_s(self, tienda):
        self.columns = [
            DataColumn(Text("DNI_empleados")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Apellidos")),
            DataColumn(Text("Telefono")),
            DataColumn(Text("Domicilio")),
            DataColumn(Text("Jornadas")),
            DataColumn(Text("Trabajos")),
            DataColumn(Text("Sueldos")),
            DataColumn(Text("DNI_jefe")),
        ]
        self.rows = []
        self.width = 1100
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT * FROM empleados WHERE tiendas LIKE '%{tienda}%' ")
        filas = c.fetchall()
        c.close()
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )
        self.update()

    def tiendas_por_propietario_s(self, propietario):
        self.columns = [
            DataColumn(Text("Nombre")),
            DataColumn(Text("Jefe")),
            DataColumn(Text("N_local")),
            DataColumn(Text("T_productos")),
            DataColumn(Text("N_empleados")),
            DataColumn(Text("empleados")),
        ]
        self.rows = []
        self.width = 1000
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT * FROM tiendas WHERE jefe = '{propietario}' ")
        filas = c.fetchall()
        c.close()
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )
        self.update()

    def empleados_por_propietario_s(self, propietario):
        self.columns = [
            DataColumn(Text("DNI_empleados")),
            DataColumn(Text("Nombre")),
            DataColumn(Text("Apellidos")),
            DataColumn(Text("Telefono")),
            DataColumn(Text("Domicilio")),
            DataColumn(Text("Jornadas")),
            DataColumn(Text("Trabajos")),
            DataColumn(Text("Sueldos")),
            DataColumn(Text("DNI_jefe")),
        ]
        self.rows = []
        self.width = 1100
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT * FROM empleados WHERE dni_jefe = '{propietario}' ")
        filas = c.fetchall()
        c.close()
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )
        self.update()

    def tiendas_s(self):
        self.columns = [
            DataColumn(Text("Nombre")),
            DataColumn(Text("Jefe")),
            DataColumn(Text("N_local")),
            DataColumn(Text("T_productos")),
            DataColumn(Text("N_empleados")),
            DataColumn(Text("Empleados")),
        ]

        self.rows = []
        db = connect_to_database()
        c = db.cursor()
        c.execute("SELECT * FROM tiendas")
        filas = c.fetchall()
        c.close()
        db.close()
        for i in filas:
            self.rows.append(
                DataRow(cells=[DataCell(Text(i[j])) for j in range(len(i))])
            )

        self.width = 1000
        self.update()
