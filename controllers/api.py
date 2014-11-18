#!/usr/bin/env python
# -*- coding: utf-8 -*-


@auth.requires_login()
def eventos():
    if request.vars['data']:
        data = request.vars['data']
        eventos = db((db.evento.data_inicio <= data) and (
            db.evento.data_final >= data)).select()
    else:
        eventos = db(db.evento).select()
    return eventos.as_json()


@auth.requires_login()
def evento():
    _id = request.args(0) or redirect(URL('erro_404'))
    evento = db(db.evento.id == _id).select().first()
    if evento:
        return evento.as_json()
    else:
        redirect(URL('erro_404'))

@auth.requires_login()
def patrocinadores():
    evento = request.args(0) or redirect(URL('erro_404'))
    if evento:
        evento = request.args(0)
        query = db.vinculo_patrocinador_evento.evento == evento
        query &= db.patrocinador.id==db.vinculo_patrocinador_evento.patrocinador
        patrocinadores = db(query).select(db.patrocinador.nome,db.patrocinador.plano)
        return patrocinadores.as_json()
    else:
        redirect(URL('erro_404'))

@auth.requires_login()
def organizadores():
    evento = request.args(0) or redirect(URL('erro_404'))
    if evento:
        evento = request.args(0)
        query = db.vinculo_organizador_evento.evento == evento
        query &= db.organizador.id==db.vinculo_organizador_evento.organizador
        query &= db.auth_user.id==db.vinculo_organizador_evento.organizador
        organizadores = db(query).select(db.auth_user.first_name,db.auth_user.last_name,
                                         db.auth_user.email, db.organizador.usuario,db.organizador.foto,
                                         db.organizador.url_facebook,db.organizador.url_twitter,
                                         db.organizador.url_gplus,db.organizador.url_Github,
                                         db.organizador.url_LinkedIn)
        return organizadores.as_json()
    else:
        redirect(URL('erro_404'))


@auth.requires_login()
def atividades():
    _id = request.args(0) or redirect(URL('erro_404'))
    atividades = db((db.atividade.evento_relacionado == _id) & (db.palestrante.id == db.atividade.palestrante)).select()
    if atividades:
        return atividades.as_json()
    else:
        redirect(URL('erro_404'))


def erro_404():
    return {'mensagem': 'Elemento não encontrado'}
