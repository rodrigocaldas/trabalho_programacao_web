# -*- coding: utf-8 -*-

from urllib2 import urlopen, HTTPError
from sqlite3 import IntegrityError
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


def palestrante():
    # verifica se url tem argumentos
    if not request.args(0):
        return HTTP(404)
    _id = request.args(0)

    try:
        # captura o evento
        chamada_api = urlopen(
            URL(c='api', f='palestrante', args=[_id], host='localhost:8000'))
        palestrante = json.loads(chamada_api.read())
        chamada_api.close()
    except HTTPError as e:
        raise HTTP(404)

    return dict(palestrante=palestrante)


@auth.requires_login()
def inscrever():
    if not request.args(0):
        return HTTP(404)
    _id = request.args(0)
    try:
        chamada_api = urlopen(
            URL(c='api', f='atividade', args=[_id], host='localhost:8000'))
        atividade = json.loads(chamada_api.read())
        chamada_api.close()
        db.vinculo_usuario_atividade.insert(
            usuario=auth.user_id, atividade=_id)
        db.commit()
        mensagem = "Parabéns, você foi inscrito em {} - {}".format(
            atividade['tipo_atividade'], atividade['titulo'])
    except HTTPError:
        db.rollback()
        raise HTTP(404)
    except IntegrityError:
        db.rollback()
        mensagem = "Você já está inscrito nesta atividade."
    return dict(mensagem=mensagem, atividade=atividade)


def horario():
    query = db.vinculo_usuario_atividade.usuario == auth.user_id
    query &= db.vinculo_usuario_atividade.atividade == db.atividade.id
    if request.vars.evento:
        query &= db.atividade.evento_relacionado == request.vars.evento
    atividades = db(query).select(orderby=db.atividade.data_hora_inicio)
    return dict(atividades=atividades)


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
