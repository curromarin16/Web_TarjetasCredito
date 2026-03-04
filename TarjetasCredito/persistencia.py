#metodos json
import json
from tarjeta_credito import TarjetaCredito
from movimiento import Movimiento
from datetime import datetime


def exportar_json(lista_tarjetas, archivo):
    """
    Metodo que guarda todos los datos en un fichero json,incluidos movimientos
    """
    with open(archivo, "w") as fichero:
        json.dump(lista_tarjetas, fichero, indent=4)

        
def importar_json(archivo):
    """
    Metodo que trae todos los datos desde un fichero json,incluidos movimientos
    """
    with open(archivo, "r") as fichero:
        datos=json.load(fichero)
    return datos



def tarjeta_dic(diccionario):
    """
    Convierte un diccionario en un objeto TarjetaCredito,
    restaurando también sus movimientos.
    """
    
    t = TarjetaCredito(
        diccionario["nombre"],
        diccionario["nif"],
        diccionario["pin"],
        diccionario["limite"],
        diccionario["numero_tarjeta"]
    )

 
    t._mes_caducidad = diccionario["mes_caducidad"]
    t._anio_caducidad = diccionario["anio_caducidad"]
    t._cvv = diccionario["cvv"]


    t._movimientos = [None] * 50
    indice = 0

    for m in diccionario.get("movimientos", []):
        if indice >= 50:
            break

        movimiento = Movimiento(m["cantidad"], m["concepto"])


        fecha = datetime.strptime(m["fecha"], "%Y-%m-%d %H:%M:%S")
        movimiento._Movimiento__fecha = fecha

        t._movimientos[indice] = movimiento
        indice += 1

    return t



        