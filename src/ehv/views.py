# -*- coding:utf-8 -*-
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from models import TipoInscricao, Inscricao, Evento, Realizacao, Apoio, Apresentacao, CampoTipoInscricao, TipoTexto, TipoAlternativa, DadosInscricao
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe

#form
from forms import NewInscricaoForm
from django import forms
from django.contrib.localflavor.br.forms import BRPhoneNumberField, BRCPFField, BRZipCodeField, BRCNPJField
from django.contrib import admin
from utils.widgets import MyDateWidget, MyCEPWidget, MyTelefoneWidget, MyCNPJWidget, MyCPFWidget

@login_required
def getTipoInscao(request, evento_id):
    if request.user.is_staff:
        try:
            retorno = []
            tipoInscricao = TipoInscricao.objects.filter(evento=evento_id)
            for ti in tipoInscricao:
                nInscritos = len(Inscricao.objects.filter(tipo_inscricao=ti))
                if ti.vagas > nInscritos:
                    retorno.append(ti)
        except:
            retorno = []

        json = serializers.serialize("json", retorno)
        return HttpResponse(json, mimetype="text/javascript")
    else:
        raise Http404


def evento(request, slug, template_name="ehv/evento.html"):
    try:
        evento = Evento.objects.get(slug=slug)
        evento.descricao = mark_safe(evento.descricao)
    except:
        raise Http404()
    
    realizacao = Realizacao.objects.filter(evento=evento)
    apoio = Apoio.objects.filter(evento=evento)

    apresentacoes = Apresentacao.objects.filter(evento=evento)
    return render_to_response(template_name, {
        'evento': evento,
        'realizacao': realizacao,
        'apoio': apoio,
        'apresentacoes': apresentacoes,
    }, context_instance=RequestContext(request))


def remove_sc(txt, codif='utf-8'):
    from unicodedata import normalize
    return normalize('NFKD', unicode(str(txt).decode(codif))).encode('ASCII','ignore')

def getInscricaoFormDinamic(tipo_inscricao):
    try:
        dados = CampoTipoInscricao.objects.filter(tipo_inscricao=tipo_inscricao).order_by('id')
        campos_dinamicos = {}
        for dado in dados:
            
            if dado.tipo == 'TX':
                try:
                    max_length = TipoTexto.objects.get(campo_tipo_inscricao=dado).tamanho
                except:
                    max_length = 255
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.CharField(required=dado.obrigatorio, max_length=max_length, label=remove_sc(dado), widget=forms.TextInput())
            elif dado.tipo == 'EM':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.EmailField(required=dado.obrigatorio, label=remove_sc(dado), widget=forms.TextInput())
            elif dado.tipo == 'SE':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.CharField(required=dado.obrigatorio, label=remove_sc(dado), widget=forms.PasswordInput())
            elif dado.tipo == 'TE':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = BRPhoneNumberField(required=dado.obrigatorio, label=remove_sc(dado), widget=MyTelefoneWidget(attrs={'style': 'width: 160px;'}))
            elif dado.tipo == 'CE':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = BRZipCodeField(required=dado.obrigatorio, label=remove_sc(dado), widget=MyCEPWidget(attrs={'style': 'width: 160px;'}))
            elif dado.tipo == 'CF':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = BRCPFField(required=dado.obrigatorio, label=remove_sc(dado), widget=MyCPFWidget(attrs={'style': 'width: 160px;'}))
            elif dado.tipo == 'CJ':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = BRCNPJField(required=dado.obrigatorio, label=remove_sc(dado), widget=MyCNPJWidget(attrs={'style': 'width: 160px;'}))
            elif dado.tipo == 'NF':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.DecimalField(required=dado.obrigatorio, decimal_places= 3, label=remove_sc(dado))
            elif dado.tipo == 'NI':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.IntegerField(required=dado.obrigatorio, label=remove_sc(dado))
            elif dado.tipo == 'DT':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.DateField(required=dado.obrigatorio, label=remove_sc(dado), widget=MyDateWidget(attrs={'style': 'width: 120px;'}))
            elif dado.tipo == 'HR':
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.TimeField(required=dado.obrigatorio, label=remove_sc(dado), widget=admin.widgets.AdminTimeWidget())
            elif (dado.tipo == 'ES') or (dado.tipo == 'ME'):
                if not dado.obrigatorio:
                    choices = [['', 'Nenhum'], ]
                else:
                    choices = []
                aux = []
                for i in range(1,11):
                    try:
                        alternativa = TipoAlternativa.objects.get(campo_tipo_inscricao=dado, numero=i).alternativa
                        aux.append(alternativa)
                        aux.append(alternativa)
                        choices.append(aux)
                        aux = []
                    except:
                        pass
                if dado.tipo == 'ES':
                    campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.ChoiceField(required=dado.obrigatorio, choices=choices, label=remove_sc(dado), widget=forms.RadioSelect())
                else:
                    campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.MultipleChoiceField(required=dado.obrigatorio, choices=choices, label=remove_sc(dado), widget=forms.CheckboxSelectMultiple())
            else:
                campos_dinamicos[remove_sc(dado).replace(" ", "_")] = forms.CharField(required=dado.obrigatorio, max_length=max_length, label=remove_sc(dado), widget=forms.TextInput())
        
        InscricaoFormDinamic = type('', (NewInscricaoForm,), campos_dinamicos)
        return InscricaoFormDinamic
    except:
        return NewInscricaoForm

@login_required
def inscricao(request, slug, template_name="ehv/inscricao.html"):
    try:
        evento = Evento.objects.get(slug=slug)
    except:
        raise Http404()

    realizacao = Realizacao.objects.filter(evento=evento)
    apoio = Apoio.objects.filter(evento=evento)
    ctx = {
        'evento': evento,
        'realizacao': realizacao,
        'apoio': apoio,
    }

    if request.method == 'GET':
        if request.GET.get('tipo_inscricao'):
            tipo_inscricao = TipoInscricao.objects.get(id=request.GET.get('tipo_inscricao'))
            if not tipo_inscricao.aberta or tipo_inscricao.estou_inscrito(request.user):
                return Http404
            ctx['tipo_inscricao'] = tipo_inscricao
            form = getInscricaoFormDinamic(request.GET.get('tipo_inscricao'))()
            ctx['form'] = form
        else:
            tipos_inscricao = TipoInscricao.objects.filter(evento=evento)
            ctx['tipos_inscricao'] = tipos_inscricao

    else:
        tipo_inscricao = TipoInscricao.objects.get(id=request.POST.get('tipo_inscricao'))
        if not tipo_inscricao.aberta or tipo_inscricao.estou_inscrito(request.user):
            return Http404
        ctx['tipo_inscricao'] = tipo_inscricao
        form = getInscricaoFormDinamic(request.POST.get('tipo_inscricao'))(request.POST)
        if form.is_valid():
            inscricao = Inscricao.objects.create(usuario=request.user, evento=tipo_inscricao.evento, tipo_inscricao=tipo_inscricao)

            dados = CampoTipoInscricao.objects.filter(tipo_inscricao=tipo_inscricao).order_by('id')
            for dado in dados:
                dado_inscricao = DadosInscricao.objects.create(inscricao=inscricao, campo=dado, resposta=form.cleaned_data[remove_sc(dado).replace(" ", "_")])
            request.user.message_set.create(message=u"Inscrição realizada com sucesso!")
            return HttpResponseRedirect(tipo_inscricao.evento.get_absolute_url())
        ctx['form'] = form

    return render_to_response(template_name, ctx, context_instance=RequestContext(request))



def all(request, template_name="ehv/all.html"):
    eventos = Evento.objects.all()
    return render_to_response(template_name, {
        'eventos': eventos,
    }, context_instance=RequestContext(request))