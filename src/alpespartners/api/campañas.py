import alpespartners.seedwork.presentacion.api as api
import json
from alpespartners.modulos.campañas.aplicacion.servicios import ServicioCampaña
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from alpespartners.modulos.campañas.aplicacion.mapeadores import MapeadorCampañaDTOJson

bp = api.crear_blueprint('campañas', '/')

@bp.route('/campañas', methods=('POST',))
def crear():
    try:
        campaña_dict = request.json

        map_campaña = MapeadorCampañaDTOJson()
        campaña_dto = map_campaña.externo_a_dto(campaña_dict)

        sr = ServicioCampaña()
        dto_final = sr.crear_campaña(campaña_dto)

        return map_campaña.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/campañas', methods=('GET',))
@bp.route('/campañas/<id>', methods=('GET',))
def dar_campaña(id=None):
    if id:
        sr = ServicioCampaña()
      
        return sr.obtener_campaña_por_id(id)
    else:
        return [{'message': 'GET!'}]