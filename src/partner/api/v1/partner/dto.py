from pydantic import BaseModel

class RegistrarPartner(BaseModel):
    nombre: str
    tipo: str
    informacion_perfil: str