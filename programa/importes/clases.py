from importes.bdd import connect_to_database


class Persona:
    def __init__(self, dni, nombre, apellidos, tlf, domicilio) -> None:
        self.DNI: str = dni
        self.nombre: str | None = nombre
        self.apellidos: str | None = apellidos
        self.telefono: str | None = tlf
        self.domicilio: str | None = domicilio


class Empleados(Persona):
    def __init__(
        self,
        dni,
        nombre,
        apellidos,
        tlf,
        domicilio,
        jornadas,
        tiendas,
        sueldos,
        dni_jefe=None,
    ) -> None:
        super().__init__(dni, nombre, apellidos, tlf, domicilio)
        if jornadas == "Jornada completa":
            self.jornadas = "1"
        elif jornadas == "3/4 de jornada":
            self.jornadas = "0.75"
        elif jornadas == "Media jornada":
            self.jornadas = "0.5"
        else:
            self.jornadas = "0.25"

        self.tiendas: str | None = tiendas
        self.sueldos: str | None = sueldos
        self.dni_jefe: str | None = dni_jefe

    def existe_empleado(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            f"SELECT DNI_empleados FROM empleados WHERE DNI_empleados= '{self.DNI}'"
        )
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) == 0:
            return True
        return False

    def jefe_is_jefe_tienda(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT jefe FROM tiendas WHERE nombre= '{self.tiendas}'")
        info = c.fetchall()
        c.execute(f"SELECT dni_jefe FROM empleados WHERE DNI_empleados= '{self.DNI}'")
        dni = c.fetchall()
        c.close()
        db.close()

        self.dni_jefe = dni[0][0]

        if info[0][0] == self.dni_jefe:
            return True
        return False

    def jornadas_posibles(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT jornadas FROM empleados WHERE DNI_empleados= '{self.DNI}'")
        info = c.fetchall()
        c.close()
        db.close()

        numeros = info[0][0].split("-")
        suma_de_jornadas = sum(float(numero) for numero in numeros)

        if suma_de_jornadas + float(self.jornadas) > 1:
            return False
        return True

    def insert_empleado(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "INSERT INTO empleados(DNI_empleados, nombre, apellidos, telefono, domicilio, jornadas, tiendas, sueldos, dni_jefe) VALUES(?,?,?,?,?,?,?,?,?)",
            (
                self.DNI,
                self.nombre,
                self.apellidos,
                self.telefono,
                self.domicilio,
                self.jornadas,
                self.tiendas,
                self.sueldos,
                self.dni_jefe,
            ),
        )

        c.close()

        db.commit()
        db.close()

    def add_trabajo_al_empleado(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            f"UPDATE empleados SET jornadas = CONCAT(jornadas, '-', '{self.jornadas}') WHERE DNI_empleados = '{self.DNI}'"
        )
        c.execute(
            f"UPDATE empleados SET tiendas = CONCAT(tiendas, '-', '{self.tiendas}') WHERE DNI_empleados = '{self.DNI}'"
        )
        c.execute(
            f"UPDATE empleados SET sueldos = CONCAT(sueldos, '-', '{self.sueldos}') WHERE DNI_empleados = '{self.DNI}'"
        )
        c.execute(
            f"UPDATE tiendas SET n_empleados = n_empleados + 1 WHERE nombre = '{self.tiendas}'"
        )
        c.execute(
            f"UPDATE tiendas SET empleados = CONCAT(empleados, '-', '{self.DNI}') WHERE nombre = '{self.tiendas}'"
        )
        c.close()
        db.commit()
        db.close()

    def del_trabajo(self):
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT tiendas FROM empleados WHERE DNI_empleados = '{self.DNI}'")

        info = c.fetchall()
        lista: list = info[0][0].split("-")

        c.execute(f"DELETE FROM empleados WHERE DNI_empleados = '{self.DNI}'")
        for i in lista:
            print(i)
            c.execute(
                f"UPDATE tiendas SET n_empleados = n_empleados -1 WHERE nombre = '{i}'"
            )
            c.execute(f"SELECT empleados FROM tiendas WHERE nombre = '{i}'")
            empleados_v = c.fetchall()
            empleados_v = empleados_v[0][0]
            print(empleados_v)
            resultado = empleados_v.replace(self.DNI, "")
            print(resultado)
            c.execute(
                f"UPDATE tiendas SET empleados = '{resultado}' WHERE nombre = '{i}'"
            )

        db.commit()
        db.close()


class Producto:
    def __init__(
        self, nombre, tienda, tipo=None, stock=None, precio_c=None, precio_v=None
    ) -> None:
        self.nombre = nombre
        self.tienda = tienda
        self.tipo = tipo
        self.stock = stock
        self.precio_c = precio_c
        self.precio_v = precio_v

    def verificar_id(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            f"SELECT nombre, tienda FROM productos WHERE nombre ='{self.nombre}' and tienda= '{self.tienda}'"
        )
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) == 0:
            return True
        return False

    def verificar_tipo(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT t_productos FROM tiendas WHERE nombre = '{self.tienda}'")
        info = c.fetchall()
        c.close()
        db.close()

        if info[0][0] == self.tipo:
            return True
        return False

    def add_producto(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "INSERT INTO productos(Nombre, Tipo, Cantidad, Tienda, Precio_compra, Precio_venta) VALUES(?,?,?,?,?,?)",
            (
                self.nombre,
                self.tipo,
                self.stock,
                self.tienda,
                self.precio_c,
                self.precio_v,
            ),
        )
        c.close()

        db.commit()

        db.close()

    def verificar_stock_0(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT Cantidad FROM productos WHERE Nombre = '{self.nombre}'")
        info = c.fetchall()
        c.close()
        db.close()

        if info[0][0] == 0:
            return True
        return False

    def del_producto(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "DELETE FROM productos WHERE Nombre=? and Tienda=?",
            (self.nombre, self.tienda),
        )
        c.close()
        db.commit()
        db.close()


class Jefe(Persona):
    def __init__(self, dni, nombre, apellidos, tlf, domicilio) -> None:
        super().__init__(dni, nombre, apellidos, tlf, domicilio)

    def buscar_duenio(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT DNI_jefe FROM jefes WHERE DNI_jefe = '{self.DNI}'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            return True
        return False

    def insertar_jefe(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "INSERT INTO jefes(DNI_jefe, nombre, apellidos, telefono, domicilio) VALUES(?,?,?,?,?)",
            (
                self.DNI,
                self.nombre,
                self.apellidos,
                self.telefono,
                self.domicilio,
            ),
        )
        c.close()

        db.commit()

        db.close()


class Tienda:
    def __init__(self, nombre, jefe=None, n_local=None, t_productos=None) -> None:
        self.nombre: str = nombre
        self.jefe: str | None = jefe
        self.n_local: int | None = n_local
        self.t_productos: str | None = t_productos

    def tienda_existente(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT nombre FROM tiendas WHERE nombre = '{self.nombre}'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            return True
        return False

    def jefe_existe(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT DNI_jefe FROM jefes WHERE DNI_jefe = '{self.jefe}'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            return True
        return False

    def max_tiendas(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT nombre FROM tiendas WHERE jefe = '{self.jefe}'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 2:
            return True
        return False

    def local_in_use(self):
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT n_local FROM tiendas WHERE n_local = '{self.n_local}'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            return True
        return False

    def insertar_tienda(self):
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "INSERT INTO tiendas(nombre, jefe, n_local, t_productos) VALUES(?,?,?,?)",
            (
                self.nombre,
                self.jefe,
                self.n_local,
                self.t_productos,
            ),
        )
        c.close()
        db.commit()
        db.close()

    def hay_productos(self):
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT Nombre FROM productos WHERE Tienda = '{self.nombre}'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            return True
        return False

    def hay_empleados(self):
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT nombre FROM empleados WHERE tiendas LIKE '%{self.nombre}%'")
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            return True
        return False

    def del_tienda(self) -> None:
        print(self.nombre)
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"DELETE FROM tiendas WHERE nombre= '{self.nombre}'")
        c.close()
        db.commit()
        db.close()

    def resultado_dinero(self) -> str:
        db = connect_to_database()
        c = db.cursor()
        c.execute(f"SELECT SUM(recibos) FROM pedidos WHERE tienda= '{self.nombre}'")
        ganancias = c.fetchall()
        c.execute(f"SELECT SUM(pago) FROM compras WHERE tienda= '{self.nombre}'")
        perdidas = c.fetchall()
        c.close()
        db.close()

        try:
            ganancias = round(float(ganancias[0][0]), 2)
        except TypeError:
            ganancias = 0

        try:
            perdidas = round(float(perdidas[0][0]), 2)
        except TypeError:
            perdidas = 0

        total = ganancias - perdidas
        total = round(total, 2)

        return (
            f"Perdidas: {perdidas} €  Ganancias: {ganancias} € Balance total: {total} €"
        )


class Pedido:
    def __init__(self, producto, tienda, cantidad) -> None:
        self.producto: str = producto
        self.tienda: str = tienda
        self.cantidad: int = cantidad

    def cantidad_disponible(self, tabla):
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            f"SELECT Cantidad FROM {tabla} WHERE Nombre = '{self.producto}' and Tienda = '{self.tienda}'"
        )
        info = c.fetchall()
        c.close()
        db.close()

        if info[0][0] >= self.cantidad:
            return True
        return False

    def producto_existe(self) -> bool:
        pass

    def add_pedido(self) -> None:
        pass


class Ventas(Pedido):
    def __init__(self, producto, tienda, cantidad) -> None:
        super().__init__(producto, tienda, cantidad)

    def producto_existe(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            f"SELECT Precio_venta FROM productos WHERE Nombre = '{self.producto}' and Tienda = '{self.tienda}'"
        )
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            self.precio_obj = float(info[0][0])
            self.precio_pedido = round(self.precio_obj * self.cantidad, 2)
            return True
        return False

    def add_pedido(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "INSERT INTO pedidos(producto, tienda, cantidad, recibos, fecha) VALUES(?,?,?,?, datetime('now'))",
            (
                self.producto,
                self.tienda,
                self.cantidad,
                self.precio_pedido,
            ),
        )
        c.execute(
            f"UPDATE productos SET Cantidad = Cantidad - {self.cantidad} WHERE Nombre = '{self.producto}' and  Tienda = '{self.tienda}'"
        )
        c.close()
        db.commit()
        db.close()


class Compras(Pedido):
    def __init__(self, producto, tienda, cantidad) -> None:
        super().__init__(producto, tienda, cantidad)

    def producto_existe(self) -> bool:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            f"SELECT Precio_compra FROM productos WHERE Nombre = '{self.producto}' and Tienda = '{self.tienda}'"
        )
        info = c.fetchall()
        c.close()
        db.close()

        if len(info) > 0:
            self.precio_obj = float(info[0][0])
            self.precio_pedido = round(self.precio_obj * self.cantidad, 2)
            return True
        return False

    def add_pedido(self) -> None:
        db = connect_to_database()
        c = db.cursor()
        c.execute(
            "INSERT INTO compras(producto, tienda, cantidad, pago, fecha) VALUES(?,?,?,?, datetime('now'))",
            (
                self.producto,
                self.tienda,
                self.cantidad,
                self.precio_pedido,
            ),
        )
        c.execute(
            f"UPDATE productos SET Cantidad = Cantidad + {self.cantidad} WHERE Nombre = '{self.producto}' and  Tienda = '{self.tienda}'"
        )
        c.close()
        db.commit()
        db.close()
