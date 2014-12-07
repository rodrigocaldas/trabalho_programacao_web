#!/usr/bin/env python
# -*- coding: utf-8 -*-


def raise404(body='', cookies=None, **headers):
    raise HTTP(404, body, cookies, **headers)


def eventos():
    if request.vars['data']:
        data = request.vars['data']
        eventos = db((db.evento.data_inicio <= data) and
                     (db.evento.data_final >= data)).select()
    else:
        eventos = db(db.evento.data_final > request.now).select(orderby=db.evento.data_inicio)
    response.headers['Content-Type'] = 'text/json'
    return eventos.as_json()


def evento():
    _id = request.args(0, cast=int)
    evento = db.evento(id=_id) or raise404()
    response.headers['Content-Type'] = 'text/json'
    return evento.as_json()


def patrocinadores():
    evento = request.args(0, cast=int)
    query = db.vinculo_patrocinador_evento.evento == evento
    query &= db.patrocinador.id == db.vinculo_patrocinador_evento.patrocinador
    patrocinadores = db(query).select(
        db.patrocinador.nome,
        db.patrocinador.plano,
        db.patrocinador.url_empresa,
        db.patrocinador.foto
    )
    response.headers['Content-Type'] = 'text/json'
    return patrocinadores.as_json()


def organizadores():
    evento = request.args(0, cast=int)
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.auth_user.id == db.vinculo_organizador_evento.organizador
    organizadores = db(query).select()
    response.headers['Content-Type'] = 'text/json'
    return organizadores.as_json()


def atividades():
    _id = request.args(0, cast=int)
    atividades = db((db.atividade.evento_relacionado == _id) &
                    (db.palestrante.id == db.atividade.palestrante)).select()
    response.headers['Content-Type'] = 'text/json'
    return atividades.as_json()


def palestrante():
    _id = request.args(0, cast=int)
    palestrante = db.palestrante(id=_id) or raise404()
    response.headers['Content-Type'] = 'text/json'
    return palestrante.as_json()


def atividade():
    _id = request.args(0, cast=int)
    atividade = db.atividade(id=_id) or raise404()
    response.headers['Content-Type'] = 'text/json'
    return atividade.as_json()
