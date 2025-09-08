from pulsar.schema import *
from dataclasses import dataclass, field
from alpespartners.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearCampañaPayload(ComandoIntegracion):
    id_usuario = String()

class ComandoCrearCampaña(ComandoIntegracion):
    data = ComandoCrearCampañaPayload()