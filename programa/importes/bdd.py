import sqlite3

crear_tabla_jefes: str = (
    "CREATE TABLE IF NOT EXISTS jefes ("
    "DNI_jefe VARCHAR(9) PRIMARY KEY,"
    "nombre VARCHAR(20) NOT NULL,"
    "apellidos VARCHAR(50) NOT NULL,"
    "telefono VARCHAR(20) NOT NULL,"
    "domicilio VARCHAR(65) NOT NULL,"
    "tiendas VARCHAR(150) NOT NULL"
    ")"
)

crear_tabla_tiendas: str = (
    "CREATE TABLE IF NOT EXISTS tiendas ("
    "nombre VARCHAR(20) PRIMARY KEY NOT NULL,"
    "jefe VARCHAR(9) NOT NULL,"
    "n_local INT NOT NULL,"
    "n_empleados INT NOT NULL,"
    "empleados VARCHAR(55),"
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


def init_database():
    db = sqlite3.connect("mercado.db")
    c = db.cursor()
    c.execute(crear_tabla_jefes)
    c.execute(crear_tabla_tiendas)
    c.execute(crear_tabla_empleados)
    db.close()


def connect_to_database() -> sqlite3.Connection:
    db = sqlite3.connect("mercado.db")
    return db


def read_dni_jefe(db, v_dni):
    c = db.cursor()
    c.execute("SELECT tiendas, dni_jefe FROM empleados WHERE DNI = ?", v_dni)
    info = c.fetchall()
    return info
