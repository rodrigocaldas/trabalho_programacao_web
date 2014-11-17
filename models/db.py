# -*- coding: utf-8 -*-

# Banco de dados
db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'])


# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth
# autenticação do usuário
auth = Auth(db)

# campos adicionais do usuário
auth.settings.extra_fields['auth_user'] = [
    Field('instituicao', label="Instituição de Ensino", length=120),
    Field('matricula', label='Matrícula', length=32),
    Field('telefone')
]


# create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

# configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

# configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
