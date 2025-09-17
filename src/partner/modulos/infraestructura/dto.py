
from sqlalchemy import Column, Integer, String, Enum
from ...config.db import Base
import enum
import uuid

class TipoPartner(enum.Enum):
    influencer = "influencer"
    affiliate = "affiliate"

class Partner(Base):
    __tablename__ = "partners"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoPartner), nullable=False)
    informacion_perfil = Column(String(255))