#bdd.py
import sqlite3
from tarjeta_credito import TarjetaCredito
from movimiento import Movimiento
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(BASE_DIR, "tarjetas_credito.db")

conexion = sqlite3.connect(RUTA_BD, check_same_thread=False)
conexion.execute("PRAGMA foreign_keys = ON")
conexion.commit()



def inicializar_bd():
    cur = conexion.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tarjetas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titular TEXT NOT NULL,
        nif TEXT NOT NULL UNIQUE,
        pin TEXT NOT NULL,
        limite REAL NOT NULL,
        numero_tarjeta TEXT NOT NULL UNIQUE,
        mes_caducidad INTEGER NOT NULL,
        anio_caducidad INTEGER NOT NULL,
        cvv INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_tarjeta TEXT NOT NULL,
        cantidad REAL NOT NULL,
        concepto TEXT NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (numero_tarjeta)
            REFERENCES tarjetas(numero_tarjeta)
            ON DELETE CASCADE
    )
    """)

    conexion.commit()
    conexion.execute("PRAGMA foreign_keys = ON")

def insert_tarjeta(tarjeta):
    """
    Inserta una nueva tarjeta de crédito en la base de datos.
    """
    cur = conexion.cursor()
    cur.execute("""
        INSERT INTO tarjetas (
            titular, nif, pin, limite, numero_tarjeta,
            mes_caducidad, anio_caducidad, cvv
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tarjeta.titular,
        tarjeta.nif,
        tarjeta.pin,
        tarjeta.limite,
        tarjeta.numero_tarjeta,
        tarjeta.mes_caducidad,
        tarjeta.anio_caducidad,
        tarjeta.cvv
    ))
    conexion.commit()


def obtener_tarjetas():
    """
    Obtiene todas las tarjetas y devuelve una lista de objetos TarjetaCredito.
    """
    cur = conexion.cursor()
    cur.execute("SELECT * FROM tarjetas")
    res = cur.fetchall()

    tarjetas = []

    for f in res:
        t = TarjetaCredito(
            f[1],  
            f[2],  
            f[3],  
            f[4],  
            f[5]   
        )

        t._mes_caducidad = f[6]
        t._anio_caducidad = f[7]
        t._cvv = f[8]

        tarjetas.append(t)

    return tarjetas

    
def delete_tarjeta(tarjeta):
    """
    Borra una tarjeta de la bdd.
    """
    cur = conexion.cursor()
    cur.execute("DELETE FROM tarjetas WHERE nif = ?", (tarjeta.nif,))
    conexion.commit()



def update_pin(tarjeta):
    """
    Actualiza el PIN de una tarjeta.
    """
    cur = conexion.cursor()
    cur.execute(
        "UPDATE tarjetas SET pin = ? WHERE numero_tarjeta = ?",
        (tarjeta.pin, tarjeta.numero_tarjeta)
    )
    conexion.commit()


#movimientos


def insertar_movimiento(tarjeta, movimiento):
    """
    Añade un nuevo movimiento a la base de datos asociado a una tarjeta de crédito.
    """
    cur = conexion.cursor()
    cur.execute("""
        INSERT INTO movimientos (
            numero_tarjeta, cantidad, concepto, fecha
        ) VALUES (?, ?, ?, ?)
    """, (
        tarjeta.numero_tarjeta,
        movimiento.cantidad,
        movimiento.concepto,
        movimiento.fecha.isoformat()
    ))
    conexion.commit()


def obtener_movimientos(numero_tarjeta):
    """
    Devuelve una lista de objetos Movimiento asociados a una tarjeta de crédito.
    """
    cur = conexion.cursor()
    cur.execute(
        "SELECT cantidad, concepto, fecha FROM movimientos WHERE numero_tarjeta=?",
        (numero_tarjeta,)
    )
    filas = cur.fetchall()

    movimientos = []

    for cantidad, concepto, fecha in filas:
        m = Movimiento(cantidad, concepto)
        m.set_fecha(datetime.fromisoformat(fecha))
        movimientos.append(m)

    return movimientos  



#metodos del main:
#gastos totales mirando la bd
def gastos_totales_bd():
    """
    Devuelve la suma total de los gastos acumulados de todas las tarjetas de crédito.
    """
    cur = conexion.cursor()
    cur.execute("""
        SELECT SUM(cantidad)
        FROM movimientos
    """)
    res = cur.fetchone()[0]

    if res is None:
        return 0
    return res

#buscar tarjeta mirando la bd
def buscar_tarjeta_por_nif(nif):
    """
    Encuentra una tarjeta de crédito por su NIF y devuelve un objeto TarjetaCredito.
    """
    cur = conexion.cursor()
    cur.execute("SELECT * FROM tarjetas WHERE nif = ?", (nif,))
    fila = cur.fetchone()

    if fila is None:
        return None

    t = TarjetaCredito(
        fila[1],  
        fila[2],  
        fila[3],  
        fila[4],  
        fila[5]   
    )
    t._mes_caducidad = fila[6]
    t._anio_caducidad = fila[7]
    t._cvv = fila[8]

    return t

#eliminar tarjeta
def eliminar_tarjeta_por_nif(nif):
    """
    Borra una tarjeta dado su nif. Devuelve el número de filas afectadas (0 si no se encontró la tarjeta, 1 si se eliminó correctamente).
    """
    cur = conexion.cursor()
    cur.execute("DELETE FROM tarjetas WHERE nif = ?", (nif,))
    conexion.commit()
    return cur.rowcount
