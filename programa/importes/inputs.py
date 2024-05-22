from flet import (
    TextField,
    colors,
    InputBorder,
    NumbersOnlyInputFilter,
    Column,
    Text,
    TextStyle,
    CrossAxisAlignment,
    MainAxisAlignment,
    FontWeight,
    Divider,
    icons,
    TextButton,
    Dropdown,
    dropdown,
    Row,
    ElevatedButton,
    IconButton,
)
from importes.clases import Producto, Empleados, Tienda, Jefe, Ventas, Compras
from importes.bdd import (
    sacar_informacion,
    connect_to_database,
)


def cambiar_rojo(TextField, text) -> bool:
    if TextField.value != "":
        TextField.label = text
        TextField.label_style = TextStyle(color=colors.BLACK)
        return True

    TextField.label = text + " es obligatorio *"
    TextField.label_style = TextStyle(color=colors.RED)

    return False


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


class Beneficios_por_tienda(Column):
    def __init__(self) -> None:
        super().__init__()
        self.tienda = Casilla_de_informacion("Tienda", "Nombre de la tienda", "str")
        self.informador = Text()
        self.informador.size = 20
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.controls = [
            Text("Tiendas", weight=FontWeight.BOLD, size=40),
            Row(
                [
                    self.tienda,
                    TextButton(
                        "Buscar",
                        icon=icons.BROWSE_GALLERY,
                        on_click=self.add_clicked,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            self.informador,
        ]

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.tienda, "Tienda")

        if operacion:
            new_tienda = Tienda(
                self.tienda.value.upper(),
            )
            if not new_tienda.tienda_existente():
                self.informador.color = colors.RED
                self.informador.value = "Esa tienda no existe"
            else:

                resultado = new_tienda.resultado_dinero()

                self.informador.color = colors.GREEN
                self.informador.value = resultado
        else:
            self.informador.color = colors.RED
            self.informador.value = " Debes insertar el nombre de la tienda"

        self.tienda.update()
        self.informador.update()


class InputTienda(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.tienda = Casilla_de_informacion("Tienda", "Nombre de la tienda", "str")
        self.jefe = Casilla_de_informacion("Jefe", "DNI del jefe", "str")
        self.n_local = Casilla_de_informacion(
            "Local", "Local en el que quiere abrir la tienda", "int"
        )
        self.tipo_productos = Casilla_de_informacion(
            "Productos", "Tipo de productos", "str"
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
            self.tipo_productos,
            Divider(height=10),
            TextButton("Añadir tienda", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]
        self.funcion = funcion

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.tienda, "Tienda")
        operacion = cambiar_rojo(self.jefe, "Jefe") and operacion
        operacion = cambiar_rojo(self.n_local, "Local") and operacion
        operacion = cambiar_rojo(self.tipo_productos, "Productos") and operacion

        if operacion:
            new_tienda = Tienda(
                self.tienda.value.upper(),
                self.jefe.value.upper(),
                self.n_local.value,
                self.tipo_productos.value.upper(),
            )
            if new_tienda.tienda_existente():
                self.informador.color = colors.RED
                self.informador.value = (
                    "Esa tienda ya existe, ingresa otro nombre distinto"
                )

            elif not new_tienda.jefe_existe():
                self.informador.color = colors.RED
                self.informador.value = (
                    "El jefe que intenta usar no existe en la base de datos"
                )

            elif new_tienda.max_tiendas():
                self.informador.color = colors.RED
                self.informador.value = "El Jefe que intenta usar ya tiene 3 tiendas"

            elif new_tienda.local_in_use():
                self.informador.color = colors.RED
                self.informador.value = "Ese local ya está en uso"

            else:

                new_tienda.insertar_tienda()

                self.funcion()
                self.tienda.value = ""
                self.jefe.value = ""
                self.n_local.value = ""
                self.tipo_productos.value = ""
                self.informador.color = colors.GREEN
                self.informador.value = "Tienda añadida con exito"
        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.tienda.update()
        self.jefe.update()
        self.n_local.update()
        self.tipo_productos.update()
        self.informador.update()


class InputJefe(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.funcion = funcion
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

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.dni_jefe, "DNI")
        operacion = cambiar_rojo(self.nombre, "Nombre") and operacion
        operacion = cambiar_rojo(self.apellidos, "Apellidos") and operacion
        operacion = cambiar_rojo(self.telefono, "Telefono") and operacion
        operacion = cambiar_rojo(self.domicilio, "Domicilio") and operacion

        if operacion:
            new_jefe = Jefe(
                self.dni_jefe.value.upper(),
                self.nombre.value,
                self.apellidos.value,
                self.telefono.value,
                self.domicilio.value,
            )

            if new_jefe.buscar_duenio():
                self.informador.color = colors.RED
                self.informador.value = "Ya existe un Dueño con ese DNI"
            elif len(self.dni_jefe.value) != 9:
                self.informador.color = colors.RED
                self.informador.value = "El DNI no tiene la longitud correcta"

            else:
                new_jefe.insertar_jefe()

                self.funcion()
                self.dni_jefe.value = ""
                self.nombre.value = ""
                self.apellidos.value = ""
                self.telefono.value = ""
                self.domicilio.value = ""
                self.informador.color = colors.GREEN
                self.informador.value = "Dueño añadido con exito"
        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.dni_jefe.update()
        self.nombre.update()
        self.apellidos.update()
        self.telefono.update()
        self.domicilio.update()
        self.informador.update()


class InputEmpleado(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.dni = Casilla_de_informacion(
            "DNI", "Documento Nacional de Identidad", "str"
        )
        self.tienda = Casilla_de_informacion("Tienda", "Nombre de la tienda", "str")
        self.nombre = Casilla_de_informacion("Nombre", "Nombre del empleado", "str")
        self.apellidos = Casilla_de_informacion(
            "Apellidos", "Apellidos del empleado", "str"
        )
        self.telefono = Casilla_de_informacion(
            "Telefono", "Telefono del empleado", "str"
        )
        self.domicilio = Casilla_de_informacion(
            "Domicilio", "Direccion del hogar", "str"
        )
        self.jornadas = Dropdown(
            options=[
                dropdown.Option("Jornada completa"),
                dropdown.Option("Media jornada"),
                dropdown.Option("3/4 de jornada"),
                dropdown.Option("Un cuarto de jornada"),
            ],
        )
        self.sueldo = Casilla_de_informacion("Sueldo", "Sueldo del empleado", "int")
        self.funcion = funcion
        self.informador = Text()

        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.controls = [
            Text("Empleados", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            Row([self.dni, self.tienda]),
            Divider(height=10),
            Row([self.nombre, self.apellidos]),
            Divider(height=10),
            Row([self.telefono, self.domicilio]),
            Divider(height=10),
            Row([self.jornadas, self.sueldo]),
            Divider(height=10),
            TextButton("Añadir empleado", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.dni, "DNI")
        operacion = cambiar_rojo(self.tienda, "Tienda") and operacion
        operacion = cambiar_rojo(self.sueldo, "Sueldo") and operacion
        operacion = (self.jornadas.value is not None) and operacion

        if operacion:

            nuevo_empleado = Empleados(
                self.dni.value.upper(),
                None,
                None,
                None,
                None,
                self.jornadas.value,
                self.tienda.value.upper(),
                self.sueldo.value,
            )

            db = connect_to_database()
            tienda_existe = sacar_informacion(
                db, "tiendas", "jefe", "nombre", self.tienda.value.upper()
            )
            db.close()
            if len(self.dni.value) != 9:
                self.informador.color = colors.RED
                self.informador.value = "El DNI debe estar formado por 9 digitos"

            elif len(tienda_existe) == 0:
                self.informador.color = colors.RED
                self.informador.value = "No existe esa tienda en la base de datos"

            elif nuevo_empleado.existe_empleado():
                operacion = cambiar_rojo(self.nombre, "Nombre")
                operacion = cambiar_rojo(self.apellidos, "Apellidos") and operacion
                operacion = cambiar_rojo(self.telefono, "Telefono") and operacion
                operacion = cambiar_rojo(self.domicilio, "Domicilio") and operacion

                if operacion:

                    dni_jefe = tienda_existe[0][0]
                    nuevo_empleado = Empleados(
                        self.dni.value.upper(),
                        self.nombre.value,
                        self.apellidos.value,
                        self.telefono.value,
                        self.domicilio.value,
                        self.jornadas.value,
                        self.tienda.value.upper(),
                        self.sueldo.value,
                        dni_jefe,
                    )
                    nuevo_empleado.insert_empleado()

                    self.funcion()
                    self.dni.value = ""
                    self.nombre.value = ""
                    self.apellidos.value = ""
                    self.telefono.value = ""
                    self.domicilio.value = ""
                    self.jornadas.value = None
                    self.tienda.value = ""
                    self.sueldo.value = ""
                    self.informador.color = colors.GREEN
                    self.informador.value = "Empleado añadido con exito"
                else:
                    self.informador.color = colors.RED
                    self.informador.value = (
                        " El DNI que intenta introducir no existe, deberá rellenar todo"
                    )

            else:

                if not nuevo_empleado.jefe_is_jefe_tienda():
                    self.informador.color = colors.RED
                    self.informador.value = (
                        " El jefe de la tienda es distinto al jefe del empleado"
                    )
                elif not nuevo_empleado.jornadas_posibles():
                    self.informador.color = colors.RED
                    self.informador.value = " Las jornadas del empleado exceden los límites de 1 jornada completa"
                else:

                    nuevo_empleado.add_trabajo_al_empleado()

                    self.funcion()
                    self.dni.value = ""
                    self.dni.label_style = TextStyle(color=colors.BLACK)
                    self.nombre.value = ""
                    self.nombre.label_style = TextStyle(color=colors.BLACK)
                    self.apellidos.value = ""
                    self.apellidos.label_style = TextStyle(color=colors.BLACK)
                    self.telefono.value = ""
                    self.telefono.label_style = TextStyle(color=colors.BLACK)
                    self.domicilio.value = ""
                    self.domicilio.label_style = TextStyle(color=colors.BLACK)
                    self.jornadas.value = None
                    self.tienda.value = ""
                    self.sueldo.value = ""
                    self.informador.color = colors.GREEN
                    self.informador.value = "Trabajo añadido con exito"

        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos jornada y con * son obligatorios"

        self.dni.update()
        self.tienda.update()
        self.nombre.update()
        self.apellidos.update()
        self.telefono.update()
        self.domicilio.update()
        self.sueldo.update()
        self.jornadas.update()
        self.informador.update()


class InputProductos(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.nombre = Casilla_de_informacion("Nombre", "Nombre del producto", "str")
        self.tienda = Casilla_de_informacion("Tienda", "Tienda de venta", "str")
        self.tipo = Casilla_de_informacion("Tipo", "Tipo de producto", "str")
        self.stock = Casilla_de_informacion("Stock", "Stock del producto", "int")
        self.precio_c = Casilla_de_informacion("Precio_C", "Precio de compra", "str")
        self.precio_v = Casilla_de_informacion("Precio_V", "Precio de venta", "str")
        self.informador = Text()
        self.funcion = funcion

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Productos", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            Row([self.nombre, self.tienda]),
            Divider(height=10),
            Row([self.tipo, self.stock]),
            Divider(height=10),
            Row([self.precio_c, self.precio_v]),
            Divider(height=10),
            TextButton("Añadir producto", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.nombre, "Nombre")
        operacion = cambiar_rojo(self.tienda, "Tienda") and operacion
        operacion = cambiar_rojo(self.tipo, "Tipo") and operacion
        operacion = cambiar_rojo(self.stock, "Stock") and operacion
        operacion = cambiar_rojo(self.precio_c, "Precio_C") and operacion
        operacion = cambiar_rojo(self.precio_v, "Precio_V") and operacion

        if operacion:
            try:
                precio_c = float(self.precio_c.value)
                precio_v = float(self.precio_v.value)
                stock = int(self.stock.value)
                seguir = True
            except:
                seguir = False

            if seguir:
                producto_nuevo = Producto(
                    self.nombre.value.upper(),
                    self.tienda.value.upper(),
                    self.tipo.value.upper(),
                    stock,
                    precio_c,
                    precio_v,
                )

                if not producto_nuevo.verificar_id():
                    self.informador.color = colors.RED
                    self.informador.value = "Ya existe ese producto en esa tienda"

                elif not producto_nuevo.verificar_tipo():
                    self.informador.color = colors.RED
                    self.informador.value = (
                        "El tipo del producto es distinto al de la tienda"
                    )

                else:
                    producto_nuevo.add_producto()
                    self.informador.color = colors.GREEN
                    self.informador.value = "Producto añadido con exito"
                    self.funcion()
                    self.nombre.value = ""
                    self.tienda.value = ""
                    self.tipo.value = ""
                    self.stock.value = ""
                    self.precio_c.value = ""
                    self.precio_v.value = ""

            else:
                self.informador.color = colors.RED
                self.informador.value = "precio_c, precio_v y stock deben ser numeros"

        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.nombre.update()
        self.tienda.update()
        self.tipo.update()
        self.stock.update()
        self.precio_c.update()
        self.precio_v.update()
        self.informador.update()


class InputPedidos(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.nombre = Casilla_de_informacion("Nombre", "Nombre del producto", "str")
        self.tienda = Casilla_de_informacion("Tienda", "Tienda de venta", "str")
        self.cantidad = Casilla_de_informacion("Cantidad", "Cantidad del pedido", "int")
        self.informador = Text()
        self.funcion = funcion

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Vender", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.nombre,
            Divider(height=10),
            self.tienda,
            Divider(height=10),
            self.cantidad,
            Divider(height=10),
            TextButton("Añadir pedido", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.nombre, "Nombre")
        operacion = cambiar_rojo(self.tienda, "Tienda") and operacion
        operacion = cambiar_rojo(self.cantidad, "Cantidad") and operacion

        if operacion:

            new_pedido = Ventas(
                self.nombre.value.upper(),
                self.tienda.value.upper(),
                int(self.cantidad.value),
            )

            if not new_pedido.producto_existe():
                self.informador.color = colors.RED
                self.informador.value = "Ese producto no existe en esa tienda"

            elif not new_pedido.cantidad_disponible("productos"):
                self.informador.color = colors.RED
                self.informador.value = (
                    "No puedes pedir mas cantidad que el stock disponible"
                )

            else:

                new_pedido.add_pedido()

                self.informador.color = colors.GREEN
                self.informador.value = "Producto añadido con exito"
                self.funcion()
                self.nombre.value = ""
                self.tienda.value = ""
                self.cantidad.value = ""

        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.nombre.update()
        self.tienda.update()
        self.cantidad.update()
        self.informador.update()


class InputCompras(Column):
    def __init__(self, funcion) -> None:
        super().__init__()
        self.nombre = Casilla_de_informacion("Nombre", "Nombre del producto", "str")
        self.tienda = Casilla_de_informacion("Tienda", "Tienda a añadir", "str")
        self.cantidad = Casilla_de_informacion("Cantidad", "Cantidad a sumar", "int")
        self.informador = Text()
        self.funcion = funcion

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Comprar", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.nombre,
            Divider(height=10),
            self.tienda,
            Divider(height=10),
            self.cantidad,
            Divider(height=10),
            TextButton("Añadir pedido", icon=icons.ADD, on_click=self.add_clicked),
            self.informador,
        ]

    def add_clicked(self, e) -> None:
        operacion = cambiar_rojo(self.nombre, "Nombre")
        operacion = cambiar_rojo(self.tienda, "Tienda") and operacion
        operacion = cambiar_rojo(self.cantidad, "Cantidad") and operacion

        if operacion:

            new_pedido = Compras(
                self.nombre.value.upper(),
                self.tienda.value.upper(),
                int(self.cantidad.value),
            )

            if not new_pedido.producto_existe():
                self.informador.color = colors.RED
                self.informador.value = "Ese producto no existe en esa tienda"

            else:

                new_pedido.add_pedido()

                self.informador.color = colors.GREEN
                self.informador.value = "Aumento de stock realizado con exito"
                self.funcion()
                self.nombre.value = ""
                self.tienda.value = ""
                self.cantidad.value = ""

        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.nombre.update()
        self.tienda.update()
        self.cantidad.update()
        self.informador.update()


class InputBusqueda(Column):
    def __init__(self, tabla) -> None:
        super().__init__()
        self.tabla = tabla
        self.productos_por_tienda = Casilla_de_informacion(
            "Consulta P x T", "Productos por Tienda", "str"
        )
        self.empleados_por_tienda = Casilla_de_informacion(
            "Consulta E x T", "Empleados por Tienda", "str"
        )
        self.tiendas_propietario = Casilla_de_informacion(
            "Consulta T x P", "Tiendas por Propietario", "str"
        )
        self.empleados_propietario = Casilla_de_informacion(
            "Consulta E x P", "Empleados por Propietario", "str"
        )
        self.tiendas = ElevatedButton(
            "Ver las tiendas del mercado", on_click=self.tiendas_s
        )
        self.informador = Text()

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Buscar", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            Row(
                [
                    self.productos_por_tienda,
                    IconButton(icon=icons.SEARCH, on_click=self.p_x_t_search),
                ]
            ),
            Divider(height=10),
            Row(
                [
                    self.empleados_por_tienda,
                    IconButton(icon=icons.SEARCH, on_click=self.e_x_t_search),
                ]
            ),
            Divider(height=10),
            Row(
                [
                    self.tiendas_propietario,
                    IconButton(icon=icons.SEARCH, on_click=self.t_x_p_search),
                ]
            ),
            Divider(height=10),
            Row(
                [
                    self.empleados_propietario,
                    IconButton(icon=icons.SEARCH, on_click=self.e_x_p_search),
                ]
            ),
            Divider(height=10),
            self.tiendas,
            Divider(height=10),
            self.informador,
        ]

    def p_x_t_search(self, e):
        self.tabla.productos_por_tienda_s(self.productos_por_tienda.value.upper())

    def e_x_t_search(self, e):
        self.tabla.empleados_por_tienda_s(self.empleados_por_tienda.value.upper())

    def t_x_p_search(self, e):
        self.tabla.tiendas_por_propietario_s(self.tiendas_propietario.value.upper())

    def e_x_p_search(self, e):
        self.tabla.empleados_por_propietario_s(self.empleados_propietario.value.upper())

    def tiendas_s(self, e):
        self.tabla.tiendas_s()


class InputDelete_Empleados(Column):
    def __init__(self) -> None:
        super().__init__()
        self.DNI = Casilla_de_informacion(
            "DNI", "Documento Nacional de Identidad", "str"
        )
        self.informador = Text()

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Empleados", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.DNI,
            Divider(height=10),
            TextButton(
                "Eliminar empleado", icon=icons.BLOCK, on_click=self.del_empleado
            ),
            self.informador,
        ]

    def del_empleado(self, e) -> None:
        operacion = cambiar_rojo(self.DNI, "Nombre")

        if operacion:

            del_empleado_v = Empleados(
                self.DNI.value.upper(), None, None, None, None, None, None, None
            )

            if del_empleado_v.existe_empleado():
                self.informador.color = colors.RED
                self.informador.value = "Ese empleado no existe en la base de datos"

            else:

                del_empleado_v.del_trabajo()

                self.informador.color = colors.GREEN
                self.informador.value = "Empleado eliminad con exito"
                self.DNI.value = ""

        else:
            self.informador.color = colors.RED
            self.informador.value = " El campo DNI es obligatiro"

        self.DNI.update()
        self.informador.update()
        self.informador.update()


class InputDelete_Productos(Column):
    def __init__(self) -> None:
        super().__init__()
        self.Nombre = Casilla_de_informacion("Nombre", "Nombre del producto", "str")
        self.tienda = Casilla_de_informacion("Tienda", "Nombre de la tienda", "str")
        self.informador = Text()

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Productos", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.Nombre,
            Divider(height=10),
            self.tienda,
            Divider(height=10),
            TextButton(
                "Eliminar producto", icon=icons.BLOCK, on_click=self.del_producto
            ),
            self.informador,
        ]

    def del_producto(self, e) -> None:
        operacion = cambiar_rojo(self.Nombre, "Nombre")
        operacion = cambiar_rojo(self.tienda, "Tienda") and operacion

        if operacion:

            del_producto_v = Producto(
                self.Nombre.value.upper(), self.tienda.value.upper()
            )

            if del_producto_v.verificar_id():
                self.informador.color = colors.RED
                self.informador.value = "Ese producto no existe en esa tienda"

            elif not del_producto_v.verificar_stock_0():
                self.informador.color = colors.RED
                self.informador.value = "No puedes borrar un producto con stock > 0"

            else:

                del_producto_v.del_producto()

                self.informador.color = colors.GREEN
                self.informador.value = "Producto eliminado con exito"
                self.Nombre.value = ""
                self.tienda.value = ""

        else:
            self.informador.color = colors.RED
            self.informador.value = " Los campos con * son obligatorios"

        self.Nombre.update()
        self.tienda.update()
        self.informador.update()


class InputDelete_Tienda(Column):
    def __init__(self) -> None:
        super().__init__()
        self.tienda = Casilla_de_informacion("Tienda", "Nombre de la tienda", "str")
        self.informador = Text()

        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.controls = [
            Text("Tienda", weight=FontWeight.BOLD, size=40),
            Divider(height=18),
            self.tienda,
            Divider(height=10),
            TextButton("Eliminar tienda", icon=icons.BLOCK, on_click=self.del_tienda),
            self.informador,
        ]

    def del_tienda(self, e) -> None:
        operacion = cambiar_rojo(self.tienda, "Tienda")

        if operacion:

            del_tienda_v = Tienda(self.tienda.value.upper())

            if not del_tienda_v.tienda_existente():
                self.informador.color = colors.RED
                self.informador.value = "Esa tienda no existe"

            elif del_tienda_v.hay_productos():
                self.informador.color = colors.RED
                self.informador.value = (
                    "No puedes borrar la tienda, todavia tiene productos"
                )
            elif del_tienda_v.hay_empleados():
                self.informador.color = colors.RED
                self.informador.value = (
                    "No puedes borrar la tienda, todavia tiene empleados"
                )
            else:

                del_tienda_v.del_tienda()

                self.informador.color = colors.GREEN
                self.informador.value = "Tienda eliminado con exito"
                self.tienda.value = ""

        else:
            self.informador.color = colors.RED
            self.informador.value = " El campo tienda es obligatorio"

        self.tienda.update()
        self.informador.update()
