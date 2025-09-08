"""DTOs para la capa de infrastructura del dominio de campañas

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de campañas

"""

from alpespartners.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia: relación muchos a muchos entre Campañas y Participantes
campañas_participantes = db.Table(
    "campañas_participantes",
    db.Model.metadata,
    db.Column("campaña_id", db.String, db.ForeignKey("campañas.id"), primary_key=True),
    db.Column("participante_id", db.String, db.ForeignKey("participantes.id"), primary_key=True)
)

class Marca(db.Model):
    __tablename__ = "marcas"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String, nullable=False)
    industria = db.Column(db.String, nullable=True)
    informacion_contacto = db.Column(db.String, nullable=True)

    # relación con campañas
    campañas = relationship("Campaña", back_populates="marca")


class Participante(db.Model):
    __tablename__ = "participantes"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = db.Column(db.String, nullable=False)  # Affiliate, Influencer, Advocate, Partner
    nombre = db.Column(db.String, nullable=False)
    informacion_perfil = db.Column(db.String, nullable=True)

    # relación con campañas
    campañas = relationship("Campaña", secondary=campañas_participantes, back_populates="participantes")


class Campaña(db.Model):
    __tablename__ = "campañas"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)  # Affiliate, Influencer, Referral, Loyalty
    estado = db.Column(db.String, nullable=False, default="draft")  # draft, active, closed
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    presupuesto = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    divisa = db.Column(db.String, nullable=False)

    # relación con Marca
    marca_id = db.Column(db.String, db.ForeignKey("marcas.id"), nullable=False)
    marca = relationship("Marca", back_populates="campañas")

    # relación con Participantes
    participantes = relationship("Participante", secondary=campañas_participantes, back_populates="campañas")
    
    def __repr__(self) -> str:
        return (
            f"<Campaña id={self.id} nombre='{self.nombre}' "
            f"fecha_inicio='{self.fecha_inicio}' fecha_fin='{self.fecha_fin}' "
        )
