import os
from tarjeta_credito import TarjetaCredito
from persistencia import exportar_json, importar_json,tarjeta_dic
import json
from bdd import *
cursor = conexion.cursor()

inicializar_bd()

def crear_tarjeta():
    """
    Pide al usuario todos los datos para generar una tarjeta nueva.
    """
    print("Bienvenido al menu para crear una tarjeta")
    titular = input("Indica tu nombre: ")
    nif = input("NIF de la persona: ")
    pin = input("Introduce el pin para la tarjeta: ")
    limite=int(input("Introduce un limite para la tarjeta: "))
    numerotarjeta = input("Introduce el numero de la tarjeta: ")
    tarjeta = TarjetaCredito(titular,nif,pin,limite,numerotarjeta)
    return tarjeta

# def buscar_tarjeta(nif:str,lista_tarjetas):
#     """
#     Busca tarjetas por el nif
#     """
#     for i in range(len(lista_tarjetas)):
#         tarjeta = lista_tarjetas[i]
#         if tarjeta.nif == nif:
#             return i
#     return -1


# def eliminar_tarjeta(lista_tarjetas, indice):
#     lista_tarjetas.pop(indice)




def gestionar_tarjeta(tarjeta):
    """
    Submenu con opciones sobre una tarjeta dada
    """
    
    while True:
        print("1-Mostrar numero de tarjeta completo")
        print("2-Mostrar nombre del titular")
        print("3-Mostrar fecha de caducidad")
        print("4-Modificar pin")
        print("5-Realizar un pago")
        print("6-Consultar Movimientos")
        print("7-Consultar gasto total")
        print("8-Volver al menu principal")
        print(" ")
        try:
            opcion = int(input("Elige una opcion (1-8):"))
            if opcion == 1:
                print("Mostrando numero de tarjeta:")
                print("-",tarjeta.numero_tarjeta)
            elif opcion == 2:
                print("Mostrando el nombre del titular:")
                print("-", tarjeta.titular)
            elif opcion == 3:
                print("Mostrando la fecha de caducidad:")
                print("-",tarjeta.anio_caducidad, "/", tarjeta.mes_caducidad)
            elif opcion == 4:
                nuevopin = input("Indique el nuevo pin: ")
                tarjeta.pin = nuevopin
                update_pin(tarjeta)
                print("Pin cambiado con exito a ",nuevopin)
            elif opcion == 5:
                try:
                    cantidad = float(input("Indique la cantidad a pagar: "))
                    concepto = input("Señale el concepto de pago: ")

                    res = tarjeta.pagar(cantidad, concepto)

                    if res:
                        print("Pago realizado con exito")
                    else:
                        print("No se puede realizar el pago (limite o movimientos llenos)")

                except ValueError as e:
                    print(e)

            elif opcion == 6:
                try:
                    numero_ultimos_movs = int(
                        input("Indique el numero de movimientos que quiere ver: ")
                    )
                    print("Mostrando movimientos:")
                    print(tarjeta.movimientos(numero_ultimos_movs))
                except ValueError as e:
                    print(e)
            elif opcion==7:
                print("Mostrando gasto total:")
                print(tarjeta.gastado())
            elif opcion == 8:
                print("Saliendo al menu principal...")
                break
        except ValueError:
            print("Debes introducir una opcion valida (1-8)")


# def gastos_totales(lista_tarjetas):
#     total = 0
#     for tarjeta in lista_tarjetas:
#         total += tarjeta.gastado()
#     return total

def main():
    #lista_tarjetas = obtener_tarjetas()
    print("Tarjetas cargadas desde la Base de Datos SQLite, total de tarjetas:", len(obtener_tarjetas()))
    while True:
        print("--- MENÚ PRINCIPAL ---")
        print("1-Crear nueva tarjeta de credito")
        print("2-Eliminar tarjeta de crédito")
        print("3-Gestionar tarjeta de crédito")
        print("4-Consultar gastos totales")
        print("5-Exportar todos los datos a JSON")
        print("6-Importar datos")
        print("7-Salir")
        print(" ")
        try:
            opcion = int(input("Elige una opción (1-7): "))
        except ValueError:
            print("Debes introducir un número.")
            continue

        #1-crear tarjeta
        if opcion == 1:
            try:
                t = crear_tarjeta()
            except ValueError as e:
                print("Error al crear la tarjeta:", e)
                continue

            t_existente = buscar_tarjeta_por_nif(t.nif)

            if t_existente is not None:
                print("Error: ya existe una tarjeta con ese NIF")
            else:
                insert_tarjeta(t)
                print("Tarjeta creada con éxito y guardada en la BD")

        #2-borrar
        elif opcion ==2:
            nif = input("Porfavor, indica el nif del titular de la cuenta a borrar: ")
            t = buscar_tarjeta_por_nif(nif)

            if t is None:
                print("Error, no se encuentra una tarjeta con ese nif.")
            else:
                confirmacion = input("Seguro? (s/n): ").lower()
                if confirmacion == "s":
                    eliminar_tarjeta_por_nif(nif)
                    print("Tarjeta eliminada de la BD.")

        #3-gestionar
        elif opcion==3:
            nif = input("Porfavor, indica el nif del titular de la cuenta a gestionar: ")
            t = buscar_tarjeta_por_nif(nif)
            if t is None:
                print("No existe tarjeta con ese NIF.")
            else:
                gestionar_tarjeta(t)

        #4-gastos totales
        elif opcion == 4:
            total = gastos_totales_bd()
            print("Gasto total:", total, "€")

        
        #5-Exportar JSON
        elif opcion == 5:
            archivo = input("Nombre del archivo JSON a guardar: ")
            if not archivo.endswith(".json"):
                archivo += ".json"

            print("Guardando datos en json...")

            tarjetas = obtener_tarjetas()
            lista_exportar = []

            for t in tarjetas:
                movs = obtener_movimientos(t.numero_tarjeta)

                lista_exportar.append(dict(
                    nombre=t.titular,
                    nif=t.nif,
                    pin=t.pin,
                    limite=t.limite,
                    numero_tarjeta=t.numero_tarjeta,
                    mes_caducidad=t.mes_caducidad,
                    anio_caducidad=t.anio_caducidad,
                    cvv=t.cvv,
                    movimientos=[
                        dict(
                            cantidad=m.cantidad,
                            concepto=m.concepto,
                            fecha=m.fecha.strftime("%Y-%m-%d %H:%M:%S")
                        ) for m in movs
                    ]
                ))

            exportar_json(lista_exportar, archivo)
            print("Datos exportados con exito a", archivo)

        #6-Importar JSON
        elif opcion == 6:
            archivo = input("Nombre del archivo JSON a importar: ")

            try:
                import os
                print("Buscando en:", os.getcwd())
                datos = importar_json(archivo)
            except FileNotFoundError:
                print("No existe ese archivo.")
                continue
            except json.JSONDecodeError:
                print("El archivo no es un JSON válido.")
                continue

            importadas = 0
            saltadas = 0

            for dic in datos:
                t = tarjeta_dic(dic)

                if buscar_tarjeta_por_nif(t.nif) is None:
                    insert_tarjeta(t)

                    for mov in dic["movimientos"]:
                        m = Movimiento(mov["cantidad"], mov["concepto"])
                        m.set_fecha(datetime.strptime(mov["fecha"], "%Y-%m-%d %H:%M:%S"))
                        insertar_movimiento(t, m)

                    importadas += 1
                else:
                    saltadas += 1

            print(f"Importación completada: {importadas} importadas, {saltadas} saltadas (NIF duplicado).")

        #7-salir
        elif opcion == 7:
            print("Saliendo del programa...")
            from bdd import conexion
            conexion.close()
            break



if __name__ == "__main__":
    main()