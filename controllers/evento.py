
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
