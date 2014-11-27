# -*- coding: utf-8 -*-

from urllib2 import urlopen, HTTPError
import json


def index():
    chamada_api = urlopen(URL(c='api', f='eventos', host='localhost:8000'))
    eventos = json.loads(chamada_api.read())
    chamada_api.close()
    return dict(eventos=eventos[:3])


def evento():

    # verifica se url tem argumentos
    if not request.args(0):
        return HTTP(404)
    _id = request.args(0)

    try:
        # captura o evento
        chamada_api = urlopen(
            URL(c='api', f='evento', args=[_id], host='localhost:8000'))
        sobre_evento = json.loads(chamada_api.read())
        chamada_api.close()

        # captura patrocinadores de um evento
        chamada_api = urlopen(
            URL(c='api', f='patrocinadores', args=[_id], host='localhost:8000')
        )
        patrocinadores = json.loads(chamada_api.read())
        chamada_api.close()

        # captura organizadores de um evento
        chamada_api = urlopen(
            URL(c='api', f='organizadores', args=[_id], host='localhost:8000')
        )
        organizadores = json.loads(chamada_api.read())
        chamada_api.close()

        # captura atividades de um evento
        chamada_api = urlopen(
            URL(c='api', f='atividades', args=[_id], host='localhost:8000')
        )
        atividades = json.loads(chamada_api.read())
        chamada_api.close()

    except HTTPError as e:
        raise HTTP(404)

    return dict(
        patrocinadores=patrocinadores,
        sobre_evento=sobre_evento,
        organizadores=organizadores,
        atividades=atividades
        )


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
