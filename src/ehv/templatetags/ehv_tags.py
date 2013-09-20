# -*- coding:utf-8 -*-
from django import template

register = template.Library()

def get_url_inscricao(tipo, user):
    if not tipo.estou_inscrito(user):
        return u'<a href="?tipo_inscricao=%s">Inscreva-se</a>' % str(tipo.id)
    else:
        return u'Você já está inscrito!'
register.simple_tag(get_url_inscricao)
