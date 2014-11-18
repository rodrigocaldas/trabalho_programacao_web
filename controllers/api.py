#!/usr/bin/env python
# -*- coding: utf-8 -*-

@auth.requires_login()
def eventos():
    if request.vars['data']:
        data = request.vars['data']
        eventos = db((db.evento.data_inicio <= data) and (db.evento.data_final >= data)).select()
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


def erro_404():
    return {'mensagem': 'Elemento não encontrado'}
