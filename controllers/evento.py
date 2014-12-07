
def index():
    eventos = db(db.evento.data_final > request.now).select()
    return dict(eventos=eventos)


@auth.requires_login()
def sou_dono():
    query = (db.vinculo_organizador_evento.organizador == auth.user_id)
    query &= (db.vinculo_organizador_evento.evento == db.evento.id)
    eventos = db(query).select(db.evento.id, db.evento.nome)
    return dict(eventos=eventos)


@auth.requires_login()
def participo():
    query = (db.vinculo_usuario_atividade.usuario == auth.user_id)
    query &= (db.atividade.id == db.vinculo_usuario_atividade.atividade)
    query &= (db.atividade.evento_relacionado == db.evento.id)
    eventos = db(query).select(db.evento.id, db.evento.nome)
    return dict(eventos=eventos)


@auth.requires_login()
def criar():
    form = SQLFORM(db.evento, submit_button='Enviar')
    if form.process().accepted:
        db.vinculo_organizador_evento.validate_and_insert(
            organizador=auth.user_id,
            evento=form.vars.id
        )
        response.flash = 'Evento criado com sucesso!'
    elif form.errors:
        response.flash = 'Formulário possui erros'
    return dict(form=form)
