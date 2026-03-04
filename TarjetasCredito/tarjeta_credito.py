#tarjeta_credito.py
from datetime import datetime
import random
import re
import copy
from movimiento import Movimiento

class TarjetaCredito:
    """
    Representa una tarjeta de crédito.
    """

    def __init__(self, titular: str, nif: str, pin: str, limite: int, numero_tarjeta: str):
        """
        Constructor de la clase TarjetaCredito.
        """
        if not self._validar_titular(titular):
            raise ValueError("Titular no válido.")

        if not self._validar_nif(nif):
            raise ValueError("NIF/CIF/NIE no válido.")

        if not self._validar_pin(pin):
            raise ValueError("PIN no válido.")

        if not (500 <= limite <= 5000):
            raise ValueError("Límite fuera de rango.")

        if not self._validar_numero_tarjeta(numero_tarjeta):
            raise ValueError("Número de tarjeta no válido.")

        self._titular = titular
        self._nif = nif
        self._pin = pin
        self._limite = limite
        self._numero_tarjeta = numero_tarjeta
        self._mes_caducidad = datetime.now().month
        self._anio_caducidad = datetime.now().year + 5
        self._cvv = random.randint(100, 999)

        self._movimientos = [None] * 50

    # constructor copia

    def __copy__(self):
        copia = TarjetaCredito(
            self._titular,
            self._nif,
            self._pin,
            self._limite,
            self._numero_tarjeta
        )
        copia._movimientos = [
            copy.copy(m) if m is not None else None
            for m in self._movimientos
        ]
        return copia

    # getters
    @property
    def titular(self):
        return self._titular

    @property
    def nif(self):
        return self._nif

    @property
    def pin(self):
        return self._pin

    @property
    def limite(self):
        return self._limite
    
    @property
    def mes_caducidad(self):
        return self._mes_caducidad

    @property
    def anio_caducidad(self):
        return self._anio_caducidad

    @property
    def numero_tarjeta(self):
        return self._numero_tarjeta

    @property
    def cvv(self):
        return self._cvv

    # setters
    @pin.setter
    def pin(self, nuevo_pin: str):
        if self._validar_pin(nuevo_pin):
            self._pin = nuevo_pin

    @limite.setter
    def limite(self, nuevo_limite: int):
        if 500 <= nuevo_limite <= 5000:
            self._limite = nuevo_limite
    

    # validaciones
    def _validar_titular(self, titular: str):
        patron = r"^[A-Za-z ]{15,80}$"
        return bool(re.match(patron, titular))

    def _validar_nif(self, nif: str):
        patron = r"^([0-9]{8}[A-Z]|[XYZ][0-9]{7}[A-Z]|[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9A-J])$"
        return bool(re.match(patron, nif))

    def _validar_pin(self, pin: str):
        patron = r"^\d{4,}$" 
        return bool(re.match(patron, pin))
    
    def _validar_numero_tarjeta(self, numero: str):
        if not numero.isdigit() or len(numero) != 16:
            return False
        return self._luhn(numero)

    @staticmethod
    def _luhn(numero: str) :
        suma = 0
        for i, digito in enumerate(reversed(numero)):
            n = int(digito)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            suma += n
        return suma % 10 == 0
    

    
    def numero_movimientos(self):
        from bdd import obtener_movimientos
        """
        Devuelve informacion sobre los ultimos movimientos que se han realizado
        para una tarjeta,pudiendo elegir cuantos.
        """
        return len(obtener_movimientos(self.numero_tarjeta))


    def gastado(self):
        from bdd import obtener_movimientos
        """
        Devuelve la cantidad total que se ha gastado
        para una tarjeta
        """        
        movimientos = obtener_movimientos(self.numero_tarjeta)
        return sum(m.cantidad for m in movimientos)

    def pagar(self, cantidad: float, concepto: str):
        from bdd import obtener_movimientos, insertar_movimiento
        """
        Genera un pago con una tarjeta y si es válido, lo guarda en la BD.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")

        movimientos = obtener_movimientos(self.numero_tarjeta)

        gastado = sum(m.cantidad for m in movimientos)
        if gastado + cantidad > self.limite:
            return False

        if len(movimientos) >= 50:
            return False
        
        m = Movimiento(cantidad, concepto)

        insertar_movimiento(self, m)

        return True

    def movimientos(self, numero_ultimos_movs: int):
        from bdd import obtener_movimientos
        """
        Devuelve los últimos N movimientos de una tarjeta.
        """
        movimientos = obtener_movimientos(self.numero_tarjeta)

        if (not isinstance(numero_ultimos_movs, int) or numero_ultimos_movs <= 0 or numero_ultimos_movs > len(movimientos)):
            raise ValueError("Debe ser un número válido")

        lista_n = movimientos[-numero_ultimos_movs:]

        resultado = ""
        for m in lista_n:
            resultado += str(m) + "\n"

        return resultado

        
    def __str__(self):
        return (
            f"Titular: {self._titular}\n"
            f"NIF: {self._nif}\n"
            f"Caducidad: {self._mes_caducidad:02d}/{self._anio_caducidad}\n"
            f"Número de tarjeta: {self._numero_tarjeta}\n"
            f"Límite: {self._limite} €\n"
            f"Gastado: {self.gastado()} €"
        )

    def __eq__(self, other):
        if not isinstance(other, TarjetaCredito):
            return False
        return self._numero_tarjeta == other._numero_tarjeta

                                      
    #metodos estaticos
    """
    Comprueba si es valido el numero de la tarjeta, devolviendo True si es asi.
    """
    @staticmethod
    def comprobar_numero_tarjeta(numero: str) -> bool:
        if not isinstance(numero, str):
            return False
        if len(numero) != 16 or not numero.isdigit():
            return False
        return TarjetaCredito._luhn(numero)
    
    """
    Calcula el digito de control del numero de la tarjeta, devolviendo ese digito
    """
    @staticmethod
    def obtener_digito_control(numeros_tarjeta:str):
        if not isinstance(numeros_tarjeta,str):
            raise ValueError("El numero deberia ser una cadena")
        if len(numeros_tarjeta)!=15 or not numeros_tarjeta.isdigit():
            raise ValueError("El numero deberia tener 15 digitos")
        for n in range(10):
            posible = numeros_tarjeta + str(n)
            if TarjetaCredito._luhn(posible):
                return str(n)
            
    
        
        