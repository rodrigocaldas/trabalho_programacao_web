# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
# Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

# your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
# this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Meu horário'), False, URL('default', 'horario.pdf'), []),
    (T('Eventos'), False, URL(), [
        (T('Criar'), False, URL('default', 'criarevento'), []),
        (T('Atividade'), False, URL(), [
            (T('Listar'), False,
             URL('default', 'listaratividade'), []),
            (T('Criar'), False,
             URL('default', 'criaratividade'), [])
        ]),
        (T('Palestrante'), False, URL(), [
            (T('Listar'), False,
             URL('default', 'listarpalestrante'), []),
            (T('Adicionar'), False,
             URL('default', 'adicionarpalestrante'), [])
        ]),
        (T('Patrocinador'), False, URL(), [
            (T('Listar'), False,
             URL('default', 'listarpatrocinadores'), []),
            (T('Adicionar'), False,
             URL('default', 'adicionarpatrocinador'), [])
        ]),
        (T('Organizador'), False, URL(), [
            (T('Listar'), False,
             URL('default', 'listarorganizadores'), []),
            (T('Adicionar'), False,
             URL('default', 'adicionarorganizadores'), [])
        ])
    ])
]
