# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
# Customize your APP title, subtitle and menus here
#########################################################################


#response.logo = A(IMG(_src=URL('static', '/images/logo.png'), _alt='WebEventos', _style='height:25px'), _href=URL('default', 'static'))
#response.subtitle = ''
#response.title = 'WebEventos'

# read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

# your http://google.com/analytics id
response.google_analytics_id = None

# #########################################################################
# this is the main application menu add/remove items as required
# #########################################################################

response.menu = [
    [IMG(_src=URL('static', '/images/logo.png'), _alt='WebEventos', _style='height:25px'), False, URL('default', 'index')],    
    (T('Home'), False, URL('default', 'index'), []),

]

if auth.is_logged_in():
    response.menu += [
        (T('Eventos'), False, '#', [
            (T('que sou dono'), False, URL('evento', 'sou_dono'), []),
            (T('que participo'), False, URL('evento', 'participo'), []),
            (T('+ criar evento'), False, URL('evento', 'criar'), []),
            (T('Listar todos'), False, URL('evento', 'index'), [])
        ]),
        (T('Palestrante'), False, '#', [
            (T('+ inserir'), False, URL('palestrante', 'inserir'), []),
            (T('Listar todos'), False, URL('palestrante', 'index'), [])
        ])

    ]
else:
    response.menu += [
        (T('Eventos'), False, '#', [
            (T('Listar todos'), False, URL('evento', 'index'), [])
        ])
    ]

    # response.menu += (T('Eventos'), False, URL(), [])
    # (T('Palestrante'), False, URL(), [
    # (T('Listar'), False,
    # URL('default', 'listarpalestrante'), []),
    # (T('Adicionar'), False,
    # URL('default', 'adicionarpalestrante'), [])
    # ]),
    # (T('Patrocinador'), False, URL(), [
    # (T('Listar'), False,
    # URL('default', 'listarpatrocinadores'), []),
    # (T('Adicionar'), False,
    # URL('default', 'adicionarpatrocinador'), [])
    # ]),
    # (T('Organizador'), False, URL(), [
    # (T('Listar'), False,
    # URL('default', 'listarorganizadores'), []),
    # (T('Adicionar'), False,
    # URL('default', 'adicionarorganizadores'), [])
    # ])
    # ])
    # ]
