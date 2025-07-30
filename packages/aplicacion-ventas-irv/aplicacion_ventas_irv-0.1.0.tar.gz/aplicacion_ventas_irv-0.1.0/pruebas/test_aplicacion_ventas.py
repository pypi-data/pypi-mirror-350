import unittest
from aplicacion_ventas.gestor_ventas import  GestorVentas
from aplicacion_ventas.exceptions import ImpuestoInvalidoError,DescuentoInvalidoError

class TestGestorVentas(unittest.TestCase):
    def test_calculo_precio_final(self):
        gestor = GestorVentas(100.0,0.05,.10)
        self.assertEqual(gestor.calcular_precio_final(),95.0)#METODO
        #ESTE METODO COMPARA SI DOS VALORES SON IGUALES, FUNCION DEVUELVE EL RESULTADO ESPERDO

    def test_impuesto_invalido(self):
        with self.assertRaises(ImpuestoInvalidoError):#METODO
            GestorVentas(100.0,1.5,0.10)
        #ESTE METODO VALIDA QUE AL GENERARSE UNA EXCEPCION DEVUELVE UN RESULTADO ESPERADO

    def test_descuento_invalido(self):
        with self.assertRaises(DescuentoInvalidoError):
            GestorVentas(100.0,0.05,1.5)
    if __name__ == "__main__":
            unittest.main()

"""
PARA EJECUTAR LAS PRUEBAS EN EL DIRECTORIO RAIZ "aplicacion_ventas"
PONER EL SIGUIENTE COMANDO EN EL COMMAND PROMPT
python -m unittest discover -s
"""