# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Meu horário'),auth.is_logged_in(),URL('default', 'horario.pdf'),[]),
    (T('Eventos'),auth.is_logged_in(),URL(),[
    	(T('Criar'),auth.is_logged_in(),URL('default', 'criarevento'),[]),
    	(T('Atividade'),auth.is_logged_in(),URL(),[
			(T('Listar'),auth.is_logged_in(),URL('default', 'listaratividade'),[]),
			(T('Criar'),auth.is_logged_in(),URL('default', 'criaratividade'),[])
		]),
    	(T('Palestrante'),auth.is_logged_in(),URL(),[
			(T('Listar'),auth.is_logged_in(),URL('default', 'listarpalestrante'),[]),
			(T('Adicionar'),auth.is_logged_in(),URL('default', 'adicionarpalestrante'),[])
		]),
    	(T('Patrocinador'),auth.is_logged_in(),URL(),[
			(T('Listar'),auth.is_logged_in(),URL('default', 'listarpatrocinadores'),[]),
			(T('Adicionar'),auth.is_logged_in(),URL('default', 'adicionarpatrocinador'),[])
		]),
    	(T('Organizador'),auth.is_logged_in(),URL(),[
			(T('Listar'),auth.is_logged_in(),URL('default', 'listarorganizadores'),[]),
			(T('Adicionar'),auth.is_logged_in(),URL('default', 'adicionarorganizadores'),[])
		])
    	])
]