# movimiento.py
from datetime import datetime
import re


class Movimiento:
    """
    Representa un movimiento bancario con una cantidad, un concepto y una fecha.
    """

    def __init__(self, cantidad: float, concepto: str):
        """
        Constructor de la clase Movimiento.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser un valor positivo.")

        if not self.__validar_concepto(concepto):
            raise ValueError("Concepto no válido.")

        self.__cantidad = cantidad
        self.__concepto = concepto
        self.__fecha = datetime.now()

    def __copy__(self):
        """
        Crea una copia del objeto Movimiento.
        """
        copia = Movimiento(self.__cantidad, self.__concepto)
        copia.__fecha = self.__fecha
        return copia

    #getters

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def concepto(self):
        return self.__concepto

    @property
    def fecha(self):
        return self.__fecha

    #setters

    @concepto.setter
    def concepto(self, nuevo_concepto: str):
        """
        Modifica el concepto si es válido.
        """
        if self.__validar_concepto(nuevo_concepto):
            self.__concepto = nuevo_concepto
    
    def set_fecha(self, fecha: datetime):
        self.__fecha = fecha


    #metodo privado

    def __validar_concepto(self, concepto: str):
        """
        Valida el concepto mediante expresión regular.
        """
        patron = r"^[A-Za-z0-9 ]{5,50}$"
        return bool(re.match(patron, concepto))

    #metodos de clase

    def __str__(self) :
        return f"Cantidad: {self.__cantidad} €, Concepto: {self.__concepto}, Fecha: {self.__fecha}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Movimiento):
            return False
        return (
            self.__cantidad == other.__cantidad and
            self.__concepto == other.__concepto and
            self.__fecha == other.__fecha
        )
