
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


@auth.requires_login()
def editar_ou_apagar():
    evento = request.args(0, cast=int)
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.vinculo_organizador_evento.organizador == auth.user_id
    if(db(query).count() == 0):
        redirect(URL('default', 'index'))
    else:
        form = SQLFORM(
            db.evento,
            evento,
            deletable=True,
            submit_button='Enviar',
            editable=True,
            upload=URL('default', 'download')
        )
        if form.process().accepted:
            response.flash = 'Evento editado com sucesso!'
        elif form.errors:
            response.flash = 'Erro no formulário'

    # form para editar  ou apagar evento
    return dict(form=form)


@auth.requires_login()
def cadastrar_organizador():
    evento = request.args(0, cast=int)
    # verifica se sou dono do evento
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.vinculo_organizador_evento.organizador == auth.user_id
    if db(query).count() == 1:
        form = SQLFORM.factory(
            Field(
                'organizador',
                widget=SQLFORM.widgets.autocomplete(
                    request,
                    db.auth_user.first_name,
                    limitby=(0, 10),
                    min_length=2,
                    help_string='Organizador'
                )
            ),
            submit_button="Enviar")
        if form.validate():
            novo_organizador = db.auth_user(first_name=form.vars.organizador)
            # verifica se já é organizadora do evento
            if novo_organizador:
                query = db.vinculo_organizador_evento.evento == evento
                query &= db.vinculo_organizador_evento.organizador == novo_organizador.id
                if db(query).count() == 1:
                    response.flash = "Esta pessoa já é organizadora deste"\
                                     " evento"
                else:
                    db.vinculo_organizador_evento.validate_and_insert(
                        organizador=novo_organizador.id,
                        evento=evento
                    )
                    response.flash = "Esta pessoa agora é também organizadora"\
                                     " do evento!"
            else:
                response.flash = "usuário inválido"
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def cadastrar_patrocinador():
    evento = request.args(0, cast=int)
    # verifica se sou dono do evento
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.vinculo_organizador_evento.organizador == auth.user_id
    if db(query).count() == 1:
        form = SQLFORM(db.patrocinador, submit_button="Enviar")
        if form.process().accepted:
            db.vinculo_patrocinador_evento.insert(
                patrocinador=form.vars.id,
                evento=evento
            )
            response.flash = "Novo patrocinador adicionado"
        elif form.errors:
            response.flash = "formulário possui erros"
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def cadastrar_atividade():
    evento = request.args(0, cast=int)
    # verifica se sou dono do evento
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.vinculo_organizador_evento.organizador == auth.user_id
    if db(query).count() == 1:
        form = SQLFORM.factory(
            db.atividade,
            db.palestrante,
            submit_button="Enviar",
            table_name='palestrante'
        )
        if form.process().accepted:
            id = db.palestrante.insert(
                **db.palestrante._filter_fields(form.vars)
            )
            form.vars.palestrante = id
            form.vars.evento_relacionado = evento
            id = db.atividade.insert(
                **db.atividade._filter_fields(form.vars)
            )
            response.flash = "Atividade inserida com sucesso"
        elif form.errors:
            response.flash = "Confira se os campos do formulário estão"\
                " corretos"
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)

@auth.requires_login()
def listar_patrocinadores():
    evento = request.args(0, cast=int)
    query = db.vinculo_patrocinador_evento.evento == evento
    query &= db.patrocinador.id == db.vinculo_patrocinador_evento.patrocinador
    patrocinadores = db(query).select()
    return dict(patrocinadores=patrocinadores)

@auth.requires_login()
def listar_organizadores():
    evento = request.args(0, cast=int)
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.auth_user.id == db.vinculo_organizador_evento.organizador
    patrocinadores = db(query).select()
    return dict(organizadores=organizadores)

@auth.requires_login()
def listar_atividades():
    _id = request.args(0, cast=int)
    query = db.atividade.evento_relacionado == _id
    query &= db.palestrante.id == db.atividade.palestrante
    organizadores = db(query).select()
    return dict(atividades=atividades)

@auth.requires_login()  
def listar_palestrantes():
    palestrantes = db(db.palestrante).select()
    return dict(palestrantes=palestrantes)

@auth.requires_login()
def cadastrar_palestrante():
    evento = request.args(0, cast=int)
    # verifica se sou dono do evento
    query = db.vinculo_organizador_evento.evento == evento
    query &= db.vinculo_organizador_evento.organizador == auth.user_id
    if db(query).count() == 1:
        form = SQLFORM(db.palestrante, submit_button="Enviar")
        if form.process().accepted:
            response.flash = "Novo palestrante adicionado"
        elif form.errors:
            response.flash = "formulário possui erros"
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)