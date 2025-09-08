from alpespartners.modulos.campañas.dominio.eventos import CampañaCreada
from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.campañas.infraestructura.despachadores import Despachador

class HandlerCampañaIntegracion(Handler):

    @staticmethod
    def handle_campaña_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-campaña')


    