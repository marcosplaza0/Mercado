import sqlite3

crear_tabla_jefes: str = (
    "CREATE TABLE IF NOT EXISTS jefes ("
    "DNI_jefe VARCHAR(9) PRIMARY KEY,"
    "nombre VARCHAR(20) NOT NULL,"
    "apellidos VARCHAR(50) NOT NULL,"
    "telefono VARCHAR(20) NOT NULL,"
    "domicilio VARCHAR(65) NOT NULL,"
    "tiendas VARCHAR(150) DEFAULT NULL"
    ")"
)


crear_tabla_tiendas: str = (
    "CREATE TABLE IF NOT EXISTS tiendas ("
    "nombre VARCHAR(20) PRIMARY KEY NOT NULL,"
    "jefe VARCHAR(9) NOT NULL,"
    "n_local INT NOT NULL,"
    "t_productos VARCHAR(50) NOT NULL,"
    "n_empleados INT DEFAULT 0,"
    "empleados VARCHAR(100) DEFAULT NULL,"
    "FOREIGN KEY (jefe) REFERENCES jefes(DNI_jefe)"
    ")"
)


crear_tabla_empleados: str = (
    "CREATE TABLE IF NOT EXISTS empleados ("
    "DNI_empleados VARCHAR(9) PRIMARY KEY,"
    "nombre VARCHAR(20) NOT NULL,"
    "apellidos VARCHAR(50) NOT NULL,"
    "telefono VARCHAR(20) NOT NULL,"
    "domicilio VARCHAR(65) NOT NULL,"
    "jornadas VARCHAR(20) NOT NULL,"
    "tiendas VARCHAR(150) NOT NULL,"
    "sueldos VARCHAR (50) NOT NULL,"
    "dni_jefe VARCHAR(9) NOT NULL,"
    "FOREIGN KEY (dni_jefe) REFERENCES jefes(DNI_jefe)"
    ")"
)


crear_tabla_productos: str = (
    "CREATE TABLE IF NOT EXISTS productos ("
    "Nombre	VARCHAR(50) NOT NULL,"
    "Tipo	VARCHAR(50) NOT NULL,"
    "Cantidad	INT,"
    "Tienda	VARCHAR(20) NOT NULL,"
    "Precio_compra	DECIMAL(11, 2) NOT NULL,"
    "Precio_venta	DECIMAL(11, 2) NOT NULL,"
    "PRIMARY KEY(Nombre,Tienda)"
    ");"
)


crear_tabla_pedidos: str = (
    "CREATE TABLE IF NOT EXISTS pedidos ("
    "ID	INTEGER NOT NULL,"
    "producto	VARCHAR(50) NOT NULL,"
    "tienda	VARCHAR(20) NOT NULL,"
    "cantidad	INTEGER NOT NULL,"
    "recibos	DECIMAL(11, 2),"
    "Fecha	DATETIME,"
    "PRIMARY KEY(ID AUTOINCREMENT)"
    ");"
)


crear_tabla_compras: str = (
    "CREATE TABLE IF NOT EXISTS compras ("
    "ID	INTEGER NOT NULL,"
    "producto	VARCHAR(50) NOT NULL,"
    "tienda	VARCHAR(20) NOT NULL,"
    "cantidad	INTEGER NOT NULL,"
    "pago	DECIMAL(11, 2) NOT NULL,"
    "fecha	DATETIME,"
    "PRIMARY KEY(ID AUTOINCREMENT)"
    ");"
)


trigger_add_tienda: str = (
    """
        CREATE TRIGGER IF NOT EXISTS add_tiendas
        AFTER INSERT ON tiendas
        BEGIN
            UPDATE jefes
            SET tiendas = CASE
                WHEN tiendas IS NULL THEN NEW.nombre
                ELSE tiendas || '-' || NEW.nombre
            END
            WHERE DNI_jefe = (SELECT jefe FROM tiendas WHERE nombre = NEW.nombre);
        END;
    """
)


trigger_del_tienda: str = (
    """
        CREATE TRIGGER IF NOT EXISTS delete_tiendas
        AFTER DELETE ON tiendas
        BEGIN
            UPDATE jefes
            SET tiendas = REPLACE(
                            REPLACE(
                                REPLACE(
                                    tiendas,
                                    '-' || OLD.nombre,
                                    ''
                                ),
                                OLD.nombre || '-',
                                ''
                            ),
                            OLD.nombre,
                            ''
                        )
            WHERE DNI_jefe = OLD.jefe;
        END;
    """
)


trigger_add_empleado_insert: str = (
    """
        CREATE TRIGGER IF NOT EXISTS update_n_empleados_insert
        AFTER INSERT ON empleados
        BEGIN
            UPDATE tiendas
            SET n_empleados = n_empleados + 1
            WHERE nombre = NEW.tiendas;
            UPDATE tiendas
            SET empleados = CASE
                WHEN empleados IS NULL THEN NEW.DNI_empleados
                ELSE empleados || '-' || NEW.DNI_empleados
            END
            WHERE nombre = NEW.tiendas;
        END;
    """
)


trigger_add_stock: str = (
    """
    CREATE TRIGGER IF NOT EXISTS update_stock_after_compra
    AFTER INSERT ON compras
    FOR EACH ROW
    BEGIN
        UPDATE productos
        SET Cantidad = Cantidad + NEW.cantidad
        WHERE Nombre = NEW.producto AND Tienda = NEW.tienda;
    END;
"""
)


def init_database():
    db = sqlite3.connect("mercado_marcos.db")
    c = db.cursor()
    c.execute(crear_tabla_jefes)
    c.execute(crear_tabla_tiendas)
    c.execute(crear_tabla_empleados)
    c.execute(crear_tabla_productos)
    c.execute(crear_tabla_pedidos)
    c.execute(crear_tabla_compras)

    c.executescript(trigger_add_tienda)

    c.executescript(trigger_del_tienda)

    c.executescript(trigger_add_empleado_insert)

    c.executescript(trigger_add_stock)

    db.commit()
    c.close()
    db.close()


def connect_to_database() -> sqlite3.Connection:
    db = sqlite3.connect("mercado_marcos.db")
    return db


def select_sencillo(db, tabla, informacion):
    c = db.cursor()
    c.execute(f"SELECT {informacion} FROM {tabla}")
    info = c.fetchall()
    c.close()
    return info


def sacar_informacion(db, tabla, informacion, campo, restriccion):
    c = db.cursor()
    c.execute(f"SELECT {informacion} FROM {tabla} WHERE {campo} = ?", (restriccion,))
    info = c.fetchall()
    c.close()
    return info


def UpdateDatabase(db, tabla, campo, restriccion, resultado, value):
    c = db.cursor()
    c.execute(f"UPDATE {tabla} set {campo}={resultado} WHERE {restriccion}=?", value)
    db.commit()
    c.close()


def Sacar_dinero_mercado():
    db = connect_to_database()
    c = db.cursor()
    c.execute("SELECT SUM(recibos) FROM pedidos")
    ganancias = c.fetchall()
    c.execute("SELECT SUM(pago) FROM compras")
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

    return f"Perdidas: {perdidas} €  Ganancias: {ganancias} € Balance total: {total} €"
