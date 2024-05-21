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

trigger_add_tienda: str = (
    """
        CREATE TRIGGER add_tiendas
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
        CREATE TRIGGER delete_tiendas
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


def init_database():
    db = sqlite3.connect("mercado_marcos.db")
    c = db.cursor()
    c.execute(crear_tabla_jefes)
    c.execute(crear_tabla_tiendas)
    c.execute(crear_tabla_empleados)

    c.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger' AND name='add_tiendas';"
    )
    trigger_exists = c.fetchone()
    if not trigger_exists:
        c.executescript(trigger_add_tienda)

    c.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger' AND name='delete_tiendas';"
    )
    trigger_exists = c.fetchone()
    if not trigger_exists:
        c.executescript(trigger_del_tienda)

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


def insert_in_tiendas(db, informacion):
    c = db.cursor()
    c.execute(
        "INSERT INTO tiendas (nombre, jefe, n_local) VALUES(?,?,?)",
        informacion,
    )
    c.close()
    db.commit()


def insert_in_jefes(db, informacion):
    c = db.cursor()
    c.execute(
        "INSERT INTO jefes (DNI_jefe, nombre, apellidos, telefono, domicilio) VALUES(?,?,?,?,?)",
        informacion,
    )
    c.close()
    db.commit()


def UpdateDatabase(db, tabla, campo, value):
    c = db.cursor()
    c.execute(f"UPDATE {tabla} set {campo}=? WHERE id=?", [value])
    db.commit()
    c.close()
