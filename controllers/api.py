#!/usr/bin/env python
# -*- coding: utf-8 -*-


def eventos():
    if request.vars['data']:
        data = request.vars['data']
        eventos = db((db.evento.data_inicio <= data) and
                     (db.evento.data_final >= data)).select()
    else:
        eventos = db(db.evento).select(orderby=db.evento.data_inicio)
    return eventos.as_json()


def evento():
    if not request.args(0):
        raise HTTP(404)
    _id = request.args(0)
    evento = db(db.evento.id == _id).select().first()
    if evento:
        return evento.as_json()
    else:
        raise HTTP(404)


def patrocinadores():
    if not request.args(0):
        raise HTTP(404)
    evento = request.args(0)
    if evento:
        evento = request.args(0)
        query = db.vinculo_patrocinador_evento.evento == evento
        query &= db.patrocinador.id == db.vinculo_patrocinador_evento.patrocinador
        patrocinadores = db(query).select(
            db.patrocinador.nome,
            db.patrocinador.plano,
            db.patrocinador.url_empresa,
            db.patrocinador.foto
        )
        return patrocinadores.as_json()
    else:
        raise HTTP(404)


def organizadores():
    if not request.args(0):
        raise HTTP(404)
    evento = request.args(0)
    if evento:
        evento = request.args(0)
        query = db.vinculo_organizador_evento.evento == evento
        query &= db.organizador.id == db.vinculo_organizador_evento.organizador
        query &= db.auth_user.id == db.vinculo_organizador_evento.organizador
        organizadores = db(query).select(
            db.auth_user.first_name, db.auth_user.last_name,
            db.auth_user.email, db.organizador.usuario, db.organizador.foto,
            db.organizador.url_facebook, db.organizador.url_twitter,
            db.organizador.url_gplus, db.organizador.url_github,
            db.organizador.url_linkedin
        )
        return organizadores.as_json()
    else:
        raise HTTP(404)


def atividades():
    if not request.args(0):
        raise HTTP(404)
    _id = request.args(0)
    atividades = db((db.atividade.evento_relacionado == _id) &
                    (db.palestrante.id == db.atividade.palestrante)).select()
    if atividades:
        return atividades.as_json()
    else:
        raise HTTP(404)


def palestrante():
    if not request.args(0):
        raise HTTP(404)
    _id = request.args(0)
    palestrante = db(db.palestrante.id == _id).select().first()
    if palestrante:
        return palestrante.as_json()
    else:
        raise HTTP(404)


def atividade():
    if not request.args(0):
        raise HTTP(404)
    _id = request.args(0)
    atividade = db(db.atividade.id == _id).select().first()
    if atividade:
        return atividade.as_json()
    else:
        raise HTTP(404)
