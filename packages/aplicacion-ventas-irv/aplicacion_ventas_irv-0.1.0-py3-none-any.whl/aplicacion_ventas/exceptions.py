"""
Controlar erores al momento de calcular impuestos o descuento
La excepcion se controlan desde los archivos impuestos y descuentos
"""
class ImpuestoInvalidoError(Exception):
    pass

class DescuentoInvalidoError(Exception):
    pass

