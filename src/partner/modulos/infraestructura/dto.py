
from sqlalchemy import Column, Integer, String, Enum
from partner.config.db import Base
import enum

class TipoPartner(enum.Enum):
    influencer = "influencer"
    empresa = "empresa"

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoPartner), nullable=False)
    informacion_perfil = Column(String(255))