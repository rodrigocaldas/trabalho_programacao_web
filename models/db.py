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

db.define_table(
    'evento',
    Field('nome', length=120, notnull=True),
    Field(
        'data_hora_inicio',
        'datetime',
        label="Data/Horário Inicial",
        notnull=True
    ),
    Field(
        'data_hora_final',
        'datetime',
        label="Data/Horário Final",
        notnull=True
    ),
    Field('localizacao', notnull=True, length=540, label="Localização"),
    Field('descricao', 'text', label="Descrição", notnull=True),
    Field(
        'url_youtube',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Youtube (https://youtube.com/seu-canal) "
    ),
    Field(
        'url_facebook',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Facebook (https://facebook.com/seu-nome)",
    ),
    Field(
        'url_twitter',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Twitter (https://twitter.com/seu-nome)",
    ),
    Field(
        'url_gplus',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Google Plus (https://plus.google.com/u/0/+Seu-nome)"
    ),
)

db.define_table(
    'organizador',
    Field('nome', length=120, notnull=True),
    Field('foto', 'upload', requires=IS_EMPTY_OR(IS_IMAGE())),
    Field(
        'url_facebook',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Facebook (https://facebook.com/seu-nome)",
    ),
    Field(
        'url_twitter',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Twitter (https://twitter.com/seu-nome)",
    ),
    Field(
        'url_gplus',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Google Plus (https://plus.google.com/u/0/+Seu-nome)"
    ),
    Field(
        'url_github',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Github (https://github.com/Seu-Git)"
    ),
    Field(
        'url_linkedin',
        requires=IS_EMPTY_OR(IS_URL()),
        label="LinkedIn "
    ),
)

db.define_table(
    'palestrante',
    Field('nome', length=120, notnull=True),
    Field('foto', 'upload', requires=IS_EMPTY_OR(IS_IMAGE())),
    Field(
        'url_facebook',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Facebook (https://facebook.com/seu-nome)",
    ),
    Field(
        'url_twitter',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Twitter (https://twitter.com/seu-nome)",
    ),
    Field(
        'url_gplus',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Google Plus (https://plus.google.com/u/0/+Seu-nome)"
    ),
    Field(
        'url_github',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Github (https://github.com/Seu-Git)"
    ),
    Field(
        'url_linkedin',
        requires=IS_EMPTY_OR(IS_URL()),
        label="LinkedIn "
    ),
    Field('bio', 'text'),
)

db.define_table(
    'atividade',
    Field(
        'tipo_atividade',
        length=12,
        requires=IS_IN_SET(['minicurso', 'workshop'],
                           zero='palestra')
    ),
    Field(
        'data_hora_inicio',
        'datetime',
        label="Data/Horário Inicial",
        notnull=True
    ),
    Field(
        'data_hora_final',
        'datetime',
        label="Data/Horário Final",
        notnull=True
    ),
)

db.define_table(
    'patrocinador',
    Field(
        'url_empresa',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Link da empresa"
    ),
    Field('foto', 'upload', requires=IS_IMAGE()),
)
