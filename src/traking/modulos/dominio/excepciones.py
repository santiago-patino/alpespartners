""" Excepciones del dominio de campañas

En este archivo usted encontrará los Excepciones relacionadas
al dominio de campañas

"""

from ...seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioEventosExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de eventos'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)