
class Participante(Record):
    id = String()
    tipo = String()
    nombre = String()
    informacion_perfil = String()

class CampaignRegistrada(Record):
    id = String()
    nombre = String()
    presupuesto = Float()
    divisa = String()
    marca_id = Long()
    participantes = Array(Participante())