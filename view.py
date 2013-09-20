from django.shortcuts import render_to_response
from django.template import RequestContext
from ehv.models import Evento
from django.utils.safestring import mark_safe


def index(request, template_name="index.html"):
    eventos = Evento.objects.all().order_by('-id')[:5:]
    for evento in eventos: evento.descricao = mark_safe(evento.descricao)
    return render_to_response(template_name, {
        'eventos': eventos,
    }, context_instance=RequestContext(request))