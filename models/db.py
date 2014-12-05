# -*- coding: utf-8 -*-

# Banco de dados
db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'])

# no generic views
response.generic_patterns = []

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
        'data_inicio',
        'date',
        label="Data Inicial",
        notnull=True
    ),
    Field(
        'data_final',
        'date',
        label="Data Final",
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
    Field('logotipo', 'upload', requires=IS_EMPTY_OR(IS_IMAGE())),
)

db.define_table(
    'organizador',
    Field('usuario', 'reference auth_user'),
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
    Field('titulo', length=120, notnull=True),
    Field('tipo_atividade',
          length=12,
          requires=IS_IN_SET(['palestra', 'minicurso', 'workshop'],
                             zero='Escolha um tipo de atividade')
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
    Field('palestrante'),
    Field('evento_relacionado'),
    Field('descricao', 'text', label="Descrição", default="")
)

db.atividade.palestrante.requires = IS_IN_DB(db, 'palestrante.id', '%(nome)s')
db.atividade.evento_relacionado.requires = IS_IN_DB(
    db,
    'evento.id',
    '%(nome)s'
)

db.define_table(
    'patrocinador',
    Field('nome', length=120, notnull=True),
    Field(
        'url_empresa',
        requires=IS_EMPTY_OR(IS_URL()),
        label="Link da empresa"
    ),
    Field('foto', 'upload', requires=IS_IMAGE()),
    Field('plano', label='Tipo de patrocínio',
          requires=IS_IN_SET(['Bronze', 'Prata', 'Ouro', 'Platina'],
                             zero='Escolha o tipo de patrocínio')
          ),
)

db.define_table(
    'vinculo_organizador_evento',
    Field('organizador', 'reference auth_user'),
    Field('evento', 'reference evento'),
)

db.vinculo_organizador_evento.organizador.requires = IS_IN_DB(
    db,
    'auth_user.id',
    '%(first_name)s'
)
db.vinculo_organizador_evento.evento.requires = IS_IN_DB(
    db,
    'evento.id',
    '%(nome)s'
)

db.define_table(
    'vinculo_patrocinador_evento',
    Field('patrocinador', 'reference patrocinador'),
    Field('evento', 'reference evento'),
)

db.vinculo_patrocinador_evento.patrocinador.requires = IS_IN_DB(
    db,
    'patrocinador.id',
    '%(nome)s'
)
db.vinculo_patrocinador_evento.evento.requires = IS_IN_DB(
    db,
    'evento.id',
    '%(nome)s'
)

db.define_table(
    'vinculo_usuario_atividade',
    Field('usuario', 'reference auth_user'),
    Field('atividade', 'reference atividade'),
    primarykey=['usuario', 'atividade']
)

db.vinculo_usuario_atividade.usuario.requires = IS_IN_DB(
    db,
    'auth_user.id',
    '%(first_name)s'
)
db.vinculo_usuario_atividade.atividade.requires = IS_IN_DB(
    db,
    'atividade.id',
    '%(titulo)s'
)
