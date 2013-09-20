# -*- coding:utf-8 -*-
from models import *
from django import forms
from django.utils.safestring import mark_safe

from filebrowser.fields import FileBrowseFormField
from utils.widgets import Readonly, CertificadoFileBrowseWidget


def remove_sc(txt, codif='utf-8'):
    from unicodedata import normalize
    return normalize('NFKD', unicode(str(txt).decode(codif))).encode('ASCII','ignore').replace(" ", "_")


class CampoTipoInscricaoForm(forms.ModelForm):
    """
        Form do modelo CampoTipoInscricao, ele contém o javascript que muda o formulário de acordo com o tipo de campo.
    """
    class Meta:
        model = CampoTipoInscricao
        
    tipo = forms.ChoiceField(choices=TIPO_CAMPO, label=u'Tipo do Campo', help_text=u'Selecione o tipo do Campo da Inscrição.', widget=forms.Select(attrs={'onChange': mark_safe("selectOptions(this);"), }))
    tamanho = forms.IntegerField(required=False, max_value=255, min_value=1, label=u'Tamanho do Campo', help_text=u'Digite o tamanho do Campo da Inscrição.')
    alternativa1 = forms.CharField(required=False, max_length=255, label=u'Alternativa 1 do Campo', help_text=u'Digite a alternativa 1 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa2 = forms.CharField(required=False, max_length=255, label=u'Alternativa 2 do Campo', help_text=u'Digite a alternativa 2 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa3 = forms.CharField(required=False, max_length=255, label=u'Alternativa 3 do Campo', help_text=u'Digite a alternativa 3 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa4 = forms.CharField(required=False, max_length=255, label=u'Alternativa 4 do Campo', help_text=u'Digite a alternativa 4 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa5 = forms.CharField(required=False, max_length=255, label=u'Alternativa 5 do Campo', help_text=u'Digite a alternativa 5 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa6 = forms.CharField(required=False, max_length=255, label=u'Alternativa 6 do Campo', help_text=u'Digite a alternativa 6 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa7 = forms.CharField(required=False, max_length=255, label=u'Alternativa 7 do Campo', help_text=u'Digite a alternativa 7 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa8 = forms.CharField(required=False, max_length=255, label=u'Alternativa 8 do Campo', help_text=u'Digite a alternativa 8 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa9 = forms.CharField(required=False, max_length=255, label=u'Alternativa 9 do Campo', help_text=u'Digite a alternativa 9 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
    alternativa10 = forms.CharField(required=False, max_length=255, label=u'Alternativa 10 do Campo', help_text=u'Digite a alternativa 10 do Campo da Inscrição.', widget=forms.TextInput(attrs={'class': 'vTextField',}))
        
    def __init__(self, *args, **kwargs):
        super(CampoTipoInscricaoForm, self).__init__(*args, **kwargs)
        if self.instance:
            if self.instance.tipo == 'TX':
                try:
                    self.fields['tamanho'].initial = TipoTexto.objects.get(campo_tipo_inscricao=self.instance).tamanho
                except:
                    pass
            elif(self.instance.tipo == 'ES' or self.instance.tipo == 'ME'):
                alternativas = TipoAlternativa.objects.filter(campo_tipo_inscricao=self.instance).order_by('numero')
                for alternativa in alternativas:
                    try:
                        self.fields['alternativa'+str(alternativa.numero)].initial = alternativa.alternativa
                    except:
                        pass



class InscricaoForm(forms.ModelForm):
    """
        Form do modelo Inscricao, ele contém o javascript para selecionar o tipo de evento de acordo com o evento.
        Ele coloca também o widget Readonly caso esteja editando.
    """
    class Meta:
        model = Inscricao


    def __init__(self, *args, **kwargs):
        super(InscricaoForm, self).__init__(*args, **kwargs)
        if self.instance:
            try:
                dados = CampoTipoInscricao.objects.filter(tipo_inscricao=self.instance.tipo_inscricao)
            except:
                dados = ()
            for dado in dados:
                try:
                    self.fields[remove_sc(dado)].initial = DadosInscricao.objects.get(inscricao=self.instance, campo=dado).resposta
                except:
                    pass
                
                
class CertificadoForm(forms.ModelForm):
    """
        Form do modelo Certificado, ele contém o javascript para selecionar o tipo de evento de acordo com o evento.
        Ele coloca também o widget Readonly caso esteja editando.
    """
    class Meta:
        model = Certificado
    
    eventos = Evento.objects.all()
    wid_evento = forms.Select(attrs={'onchange': mark_safe("getAjax('/get/tipoinscricao/'+this.value, 'id_tipo_inscricao');"), })
    evento = forms.ModelChoiceField(queryset=eventos ,label=u'Evento', help_text='Selecione o Evento da Inscricao.', widget=wid_evento)
    template = FileBrowseFormField(widget=CertificadoFileBrowseWidget(attrs={'format': 'Image', 'directory' : '', 'extensions': ''}))
    
    def __init__(self, *args, **kwargs):
        super(CertificadoForm, self).__init__(*args, **kwargs)
        if self.instance:
            try:
                if self.instance.evento:
                    self.fields['evento'].widget = Readonly(model=Evento)
                    self.fields['tipo_inscricao'].widget = Readonly(model=TipoInscricao)
            except:
                pass
            

class CampoCertificadoForm(forms.ModelForm):
    
    class Meta:
        model = CampoCertificado
        
    x = forms.IntegerField(min_value=0, label=u'Coord. X', help_text=u'Digite a coordenada x deste campo do template do Certificado.', widget=forms.TextInput(attrs={'style': 'width: 50px;',}))
    y = forms.IntegerField(min_value=0, label=u'Coord. Y', help_text=u'Digite a coordenada y deste campo do template do Certificado.', widget=forms.TextInput(attrs={'style': 'width: 50px;',}))
    tamanho = forms.IntegerField(min_value=1, label=u'Tam. da letra', help_text=u'Digite o tamanho da letra deste campo do Certificado.', widget=forms.TextInput(attrs={'style': 'width: 70px;',}))



class NewInscricaoForm(forms.ModelForm):

    class Meta:
        model = Inscricao
        exclude = ('usuario', 'evento', 'tipo_inscricao', 'data', )