
def index():
    palestrantes = db(db.palestrante).select()
    return dict(palestrantes=palestrantes)

@auth.requires_login()
def inserir():
    form = SQLFORM(db.palestrante, submit_button='Enviar')
    if form.process().accepted:
        response.flash = 'Palestrante inserido com sucesso!'
    elif form.errors:
        response.flash = 'Formulário possui erros'
    return dict(form=form)
