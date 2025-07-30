class Precios:
    """
    @statucnetgod = decorador

    #metodo estatico dentro de una clase, no dependen de una instancia particular
    de la clase y no tienen acceso a los atributos o metodos de la  instancia
    es decir no puede acceder a self

    """
    @staticmethod

    def calcular_precio_final(precio_base, impuesto, descuento): #no hay constructor ni atributo
        return precio_base + impuesto - descuento

