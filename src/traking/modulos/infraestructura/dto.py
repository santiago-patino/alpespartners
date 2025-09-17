
from sqlalchemy import Column, Integer, String, Enum, DateTime, BigInteger
from ...config.db import Base
from datetime import datetime
import uuid

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    id_partner = Column(String(100), nullable=False)
    id_campana = Column(String(100), nullable=False)
    #fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha = Column(BigInteger, nullable=False)