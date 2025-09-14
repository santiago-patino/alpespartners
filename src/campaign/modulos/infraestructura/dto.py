
from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from campaign.config.db import Base
import enum
import uuid

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    presupuesto = Column(Float, nullable=False)
    divisa = Column(String(10), nullable=False)
    marca_id = Column(String(36), nullable=False)
    participantes = Column(JSON, nullable=True)
    #participantes = relationship("Participante", back_populates="campaign")
    
# class Participante(Base):
#     __tablename__ = "participantes"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     tipo = Column(String(50), nullable=True)
#     nombre = Column(String(100), nullable=False)
#     informacion_perfil = Column(String(36), ForeignKey("campaigns.id"))

#     campaign = relationship("Campaign", back_populates="participantes")