from traking.seedwork.aplicacion.handlers import Handler
from traking.modulos.infraestructura.despachadores import Despachador

class HandlerEventoDominio(Handler):

    @staticmethod
    def handle_evento_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'evento-traking')
        print('================ EVENTO CREADO ===========')
        
    @staticmethod
    def handle_evento_fallido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'evento-traking')
        print('================ EVENTO FALLIDO ===========')
        

    