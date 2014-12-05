# -*- coding: utf-8 -*-


from sqlite3 import IntegrityError
import requests


def index():
    chamada_api = requests.get(
        URL(
            c='api',
            f='eventos',
              host='localhost:8000'
        )
    )
    eventos = chamada_api.json()
    return dict(eventos=eventos[:3])


def evento():

    _id = request.args(0, cast=int)

    # captura o evento
    sobre_evento = requests.get(
        URL(
            c='api',
            f='evento',
            args=[_id],
            host='localhost:8000'
        )
    ).json()

    # captura patrocinadores de um evento
    patrocinadores = requests.get(
        URL(
            c='api',
            f='patrocinadores',
            args=[_id],
            host='localhost:8000'
        )
    ).json()

    # captura organizadores de um evento
    organizadores = requests.get(
        URL(
            c='api',
            f='organizadores',
            args=[_id],
            host='localhost:8000'
        )
    ).json()

    # captura atividades de um evento
    atividades = requests.get(
        URL(
            c='api',
            f='atividades',
            args=[_id],
            host='localhost:8000'
        )
    ).json()

    return dict(
        patrocinadores=patrocinadores,
        sobre_evento=sobre_evento,
        organizadores=organizadores,
        atividades=atividades
    )


def palestrante():

    _id = request.args(0, cast=int)

    palestrante = requests.get(
        URL(
            c='api',
            f='palestrante',
            args=[_id],
            host='localhost:8000'
        )
    ).json()

    return dict(palestrante=palestrante)


@auth.requires_login()
def inscrever_em_atividade():

    _id = request.args(0)

    atividade = requests.get(
        URL(
            c='api',
            f='atividade',
              args=[_id],
            host='localhost:8000'
        )
    ).json()
    try:
        db.vinculo_usuario_atividade.validate_and_insert(
            usuario=auth.user_id,
            atividade=_id
        )
        mensagem = "Parabéns, você foi inscrito em {} - {}".format(
            atividade['tipo_atividade'],
            atividade['titulo']
        )
    except IntegrityError:
        mensagem = "Você já está inscrito nesta atividade."
    return dict(mensagem=mensagem, atividade=atividade)


@auth.requires_login(
    otherwise=lambda: redirect(
        URL(
            f='user',
            args=['login'],
              vars={'_next': request.url},
            extension='html')
    )
)
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
