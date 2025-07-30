from .exceptions import DescuentoInvalidoError

class Descuentos:
    def __init__(self,porcentaje): #CONSTRUCTOR CON 1 ATRIBUTO
        if not (0<=porcentaje<=1):
            raise DescuentoInvalidoError("El porcentaje de descuento debe "
                                         "estar entre 0 y 1")
        self.porcentaje = porcentaje

    def aplicar_descuento(self, precio):
        return precio * self.porcentaje
