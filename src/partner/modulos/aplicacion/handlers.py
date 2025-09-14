from partner.modulos.vuelos.dominio.eventos.reservas import ReservaCreada
from partner.seedwork.aplicacion.handlers import Handler

class HandlerReservaDominio(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        print('================ RESERVA CREADA ===========')
        

    