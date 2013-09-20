# -*- coding:utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django import forms
from django.contrib.localflavor.br.forms import BRPhoneNumberField, BRCPFField, BRZipCodeField, BRCNPJField

from models import *
from forms import *

from report.actions import report_generic, report_generic_detailed
from actions import report_list, make_certificado_tipo, make_certificado_inscricao


from django.http import HttpResponse


def remove_sc(txt, codif='utf-8'):
    from unicodedata import normalize
    return normalize('NFKD', unicode(str(txt).decode(codif))).encode('ASCII','ignore').replace(" ", "_")


class AdminEvento(admin.ModelAdmin):
    """
    ModelAdmin AdminEvento, admin do modelo Evento
    """

    class Media:
        js = [  '%s/tinymce/jscripts/tiny_mce/tiny_mce.js' % settings.ADMIN_MEDIA_PREFIX,
                '%s/tinymce_setup/tinymce_setup.js' % settings.ADMIN_MEDIA_PREFIX,
            ]

    list_display = ('id', 'logo', 'nome', 'slug', 'tags', 'acoes', )
    search_fields = ('id', 'nome', 'slug', 'descricao', 'tags', )
    list_filter = ('tags',)

    list_report = ('nome', 'slug', 'tags', 'descricao',)
    actions = [report_generic, ]
    
    fieldsets_report = [
        (u'Evento',             {'classes' : ('collapse open', ), 'fields' : ('nome', 'logo', ), }, ),
        (u'Descrição/Tags',          {'classes' : ('collapse open', ), 'fields' : ('descricao', 'tags',), }, ),
       ]
    list_report = ('id', 'logo', 'nome', 'slug', 'tags', )
    actions = [report_generic, report_generic_detailed, ]

    save_on_top = True
    
    fieldsets = [
        (u'Evento',             {'classes' : ('collapse open', ), 'fields' : ('nome', 'logomarca', ), }, ),
        (u'Descrição/Tags',          {'classes' : ('collapse open', ), 'fields' : ('descricao', 'tags',), }, ),
       ]
    
    def queryset(self, request):
        qs = super(AdminEvento, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        obj.save()
        


class AdminRealizacao(admin.ModelAdmin):
    """
    ModelAdmin AdminRealizacao, admin do modelo Apoio
    """
    
    list_display = ('id', 'nome', 'logo', 'link', 'evento', 'acoes', )
    search_fields = ('id', 'nome', 'link', 'evento__nome', )
    raw_id_fields = ('evento', )
    save_on_top = True
    
    fieldsets = [
        (u'Realização',          {'classes' : ('collapse open', ), 'fields' : ('nome', 'evento', 'logomarca', 'link', ), }, ),
       ]

    fieldsets_report = [
        (u'Realização',          {'classes' : ('collapse open', ), 'fields' : ('nome', 'evento', 'logomarca', 'link', ), }, ),
       ]
    list_report = ('id', 'nome', 'logo', 'link', 'evento',)
    actions = [report_generic, report_generic_detailed, ]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evento":
            eventos = Evento.objects.filter(autor=request.user)
            kwargs["queryset"] = eventos
        return super(AdminRealizacao, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def queryset(self, request):
        qs = super(AdminRealizacao, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__autor=request.user)
    
    
    
class AdminApoio(admin.ModelAdmin):
    """
    ModelAdmin AdminApoio, admin do modelo Apoio
    """

    list_display = ('id', 'nome', 'logo', 'link', 'evento', 'acoes', )
    search_fields = ('id', 'nome', 'link', 'evento__nome', )
    raw_id_fields = ('evento', )
    save_on_top = True
    
    fieldsets = [
        (u'Apoio',          {'classes' : ('collapse open', ) , 'fields' : ('nome', 'evento', 'logomarca', 'link', ), }, ),
       ]

    fieldsets_report = [
        (u'Apoio',          {'classes' : ('collapse open', ) , 'fields' : ('nome', 'evento', 'logomarca', 'link', ), }, ),
       ]
    list_report = ('id', 'nome', 'logo', 'link', 'evento',)
    actions = [report_generic, report_generic_detailed, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "evento":
            eventos = Evento.objects.filter(autor=request.user)
            kwargs["queryset"] = eventos
        return super(AdminApoio, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def queryset(self, request):
        qs = super(AdminApoio, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__autor=request.user)



class AdminApresentador(admin.ModelAdmin):
    """
    ModelAdmin AdminApresentacao, admin do modelo Apresentacao
    """        
    list_display = ('id', 'nome', 'email', 'foto_apresentador', 'link', 'tags', 'acoes', )
    search_fields = ('id', 'nome', 'email', 'link', 'descricao', 'tags',)
    list_filter = ('tags', )
    save_on_top = True
    
    
    fieldsets = [
        (u'Apresentador',       {'classes' : ('collapse open',), 'fields' : ('nome', 'email', 'link', ), }, ),
        (u'Descrição/Tags',          {'classes' : ('collapse open',), 'fields' : ('descricao', 'tags',), }, ),
        ]

    fieldsets_report = [
        (u'Apresentador',       {'classes' : ('collapse open',), 'fields' : ('nome', 'email', 'link', ), }, ),
        (u'Descrição/Tags',          {'classes' : ('collapse open',), 'fields' : ('descricao', 'tags',), }, ),
        ]
    list_report = ('id', 'nome', 'email', 'foto_apresentador', 'link', 'tags', )
    actions = [report_generic, report_generic_detailed, ]

    def queryset(self, request):
        qs = super(AdminApresentador, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        obj.save()


class InlineDataHora(admin.TabularInline):
    """
    Inline InlineDataHora, admin inline do modelo DataHora.
    O inline será usado no admin AdminApresentacao.
    """
    model = DataHora
    extra = 1
    classes = ('collapse open',)
    # Grappelli Options
    allow_add = True
    
    
class AdminApresentacao(admin.ModelAdmin):
    """
    ModelAdmin AdminApresentacao, admin do modelo Apresentacao
    """    
    list_display = ('id', 'titulo', 'tipo', 'evento', 'local', 'tags', 'acoes', )
    search_fields = ('id', 'titulo', 'tipo', 'descricao', 'evento__nome', 'local', 'tags',)
    list_filter = ('tipo', 'tags',)
    filter_horizontal = ('apresentadores', )
    radio_fields = {"tipo": admin.HORIZONTAL}
    raw_id_fields = ('evento', )
    save_on_top = True
    
    inlines = [InlineDataHora, ]
    
    fieldsets = [
        (u'Apresentação',       {'classes' : ('collapse open',), 'fields' : ('titulo', 'tipo', 'evento', ), }, ),
        (u'Apresentadores',     {'classes' : ('collapse open',), 'fields' : ('apresentadores', ), }, ),
        (u'Local/Descrição/Tags',          {'classes' : ('collapse open',), 'fields' : ('local', 'descricao', 'tags',), }, ),
        ]

    fieldsets_report = [
        (u'Apresentação',       {'classes' : ('collapse open',), 'fields' : ('titulo', 'tipo', 'evento', ), }, ),
        (u'Apresentadores',     {'classes' : ('collapse open',), 'fields' : ('apresentadores', ), }, ),
        (u'Local/Descrição/Tags',          {'classes' : ('collapse open',), 'fields' : ('local', 'descricao', 'tags',), }, ),
        ]
    list_report = ('id', 'titulo', 'tipo', 'evento', 'local', 'tags', )
    actions = [report_generic, report_generic_detailed, ]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "evento":
                eventos = Evento.objects.filter(autor=request.user)
                kwargs["queryset"] = eventos
        return super(AdminApresentacao, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "apresentadores":
                kwargs["queryset"] = Apresentador.objects.filter(autor=request.user)
        return super(AdminApresentacao, self).formfield_for_manytomany(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(AdminApresentacao, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__autor=request.user)

    def add_view(self, request, form_url="", extra_context=None):
        self.readonly_fields = ()
        return super(AdminApresentacao, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        self.readonly_fields = ("evento", )
        return super(AdminApresentacao, self).change_view(request, object_id, extra_context)



class InlineCampoTipoInscricao(admin.StackedInline):
    """
    Inline InlineCampoTipoInscricao, admin inline do modelo CampoTipoInscricao.
    O inline será usado no admin AdminTipoInscricao.
    """
    class Media:
        js = (
            settings.MEDIA_URL + 'admin/js/campotipoinscricao.js',
        )
        
    model = CampoTipoInscricao
    form = CampoTipoInscricaoForm
    extra = 1
    classes = ('collapse open',)
    fieldsets = [
        (u'Campo',  {'classes' : ('isTrue',), 'fields' : ('nome', 'obrigatorio', 'tipo',)}),
        (u'Tamanho',      {'classes' : ('thisTamanho isFalse',), 'fields' : ('tamanho', )}),
        (u'Alternativas',      {'classes' : ('thisAlternativas isFalse',), 'fields' : ('alternativa1', 'alternativa2', 'alternativa3', 'alternativa4', 'alternativa5', 'alternativa6', 'alternativa7', 'alternativa8', 'alternativa9', 'alternativa10',)}),
        ]
    # Grappelli Options
    allow_add = True
    
    
    
class AdminTipoInscricao(admin.ModelAdmin):
    """
    ModelAdmin AdminTipoInscricao, admin do modelo TipoInscricao
    """
    list_display = ('id', 'nome', 'evento', 'publicado', 'vagas', 'data_inicio_inscricao', 'data_fim_inscricao', 'aberta', 'vagas_abertas', 'acoes', )
    search_fields = ('id', 'nome', 'evento__nome', )
    list_filter = ('publicado', )
    filter_horizontal = ('apresentacoes', )
    raw_id_fields = ('evento', )
    save_on_top = True
    
    inlines = [InlineCampoTipoInscricao, ]
    
    fieldsets = [
        (u'Tipo de Inscrição',  {'classes' : ('collapse open',), 'fields' : ('nome', 'evento', 'publicado', 'vagas', ('data_inicio_inscricao', 'data_fim_inscricao',), )}),
        (u'Apresentações',      {'classes' : ('collapse open',), 'fields' : ('apresentacoes', )}),
        ]

    fieldsets_report = [
        (u'Tipo de Inscrição',  {'classes' : ('collapse open',), 'fields' : ('nome', 'evento', 'publicado', 'vagas', ('data_inicio_inscricao', 'data_fim_inscricao',), )}),
        (u'Apresentações',      {'classes' : ('collapse open',), 'fields' : ('apresentacoes', )}),
        ]
    list_report = ('id', 'nome', 'evento', 'publicado', 'vagas', 'data_inicio_inscricao', 'data_fim_inscricao', 'aberta', 'vagas_abertas', )
    actions = [report_generic, report_generic_detailed, report_list, make_certificado_tipo, ]


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "evento":
                eventos = Evento.objects.filter(autor=request.user)
                kwargs["queryset"] = eventos
        return super(AdminTipoInscricao, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "apresentacoes":
                kwargs["queryset"] = Apresentacao.objects.filter(evento__autor=request.user)
        return super(AdminTipoInscricao, self).formfield_for_manytomany(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(AdminTipoInscricao, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__autor=request.user)

    def add_view(self, request, form_url="", extra_context=None):
        self.readonly_fields = ()
        return super(AdminTipoInscricao, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        self.readonly_fields = ("evento", )
        return super(AdminTipoInscricao, self).change_view(request, object_id, extra_context)
    
    def save_formset(self, request, form, formset, change):
        super(AdminTipoInscricao, self).save_formset(request, form, formset, change)
        for item_campo_form in formset.forms:
            if not item_campo_form.cleaned_data:
                continue
            if item_campo_form.instance.tipo == 'TX':
                if item_campo_form.cleaned_data['tamanho']:
                    try:
                        tamanho = TipoTexto.objects.get_or_create(campo_tipo_inscricao=item_campo_form.instance)[0]
                        tamanho.tamanho = item_campo_form.cleaned_data['tamanho']
                        tamanho.save()
                    except:
                        pass
                else:
                    try:
                        TipoTexto.objects.get(campo_tipo_inscricao=item_campo_form.instance).delete()
                    except:
                        pass
            elif(item_campo_form.instance.tipo == 'ES' or item_campo_form.instance.tipo == 'ME'):
                for i in range(1,11):
                    if item_campo_form.cleaned_data['alternativa'+str(i)]:
                        try:
                            alternativa = TipoAlternativa.objects.get_or_create(campo_tipo_inscricao=item_campo_form.instance, numero=i)[0]
                            alternativa.alternativa = item_campo_form.cleaned_data['alternativa'+str(i)]
                            alternativa.save()
                        except:
                            pass
                    else:
                        try:
                            TipoAlternativa.objects.get(campo_tipo_inscricao=item_campo_form.instance, numero=i).delete()
                        except:
                            pass
                        
        super(AdminTipoInscricao, self).save_formset(request, form, formset, change)
    


def getInscricaoFormDinamic(id_inscricao):
    try:
        inscricao = Inscricao.objects.get(id=id_inscricao)
        dados = CampoTipoInscricao.objects.filter(tipo_inscricao=inscricao.tipo_inscricao).order_by('id')
        campos_dinamicos = {}
        for dado in dados:
            
            if dado.tipo == 'TX':
                try:
                    max_length = TipoTexto.objects.get(campo_tipo_inscricao=dado).tamanho
                except:
                    max_length = 255
                campos_dinamicos[remove_sc(dado)] = forms.CharField(required=dado.obrigatorio, max_length=max_length, label=remove_sc(dado), widget=forms.TextInput(attrs={'class': 'vTextField'}))
            elif dado.tipo == 'EM':
                campos_dinamicos[remove_sc(dado)] = forms.EmailField(required=dado.obrigatorio, label=remove_sc(dado), widget=forms.TextInput(attrs={'class': 'vTextField'}))
            elif dado.tipo == 'SE':
                campos_dinamicos[remove_sc(dado)] = forms.CharField(required=dado.obrigatorio, label=remove_sc(dado), widget=forms.PasswordInput())
            elif dado.tipo == 'TE':
                campos_dinamicos[remove_sc(dado)] = BRPhoneNumberField(required=dado.obrigatorio, label=remove_sc(dado), widget=forms.TextInput(attrs={'class': 'vTextField'}))
            elif dado.tipo == 'CE':
                campos_dinamicos[remove_sc(dado)] = BRZipCodeField(required=dado.obrigatorio, label=remove_sc(dado))
            elif dado.tipo == 'CF':
                campos_dinamicos[remove_sc(dado)] = BRCPFField(required=dado.obrigatorio, label=remove_sc(dado))
            elif dado.tipo == 'CJ':
                campos_dinamicos[remove_sc(dado)] = BRCNPJField(required=dado.obrigatorio, label=remove_sc(dado))
            elif dado.tipo == 'NF':
                campos_dinamicos[remove_sc(dado)] = forms.DecimalField(required=dado.obrigatorio, decimal_places= 3, label=remove_sc(dado))
            elif dado.tipo == 'NI':
                campos_dinamicos[remove_sc(dado)] = forms.IntegerField(required=dado.obrigatorio, label=remove_sc(dado))
            elif dado.tipo == 'DT':
                campos_dinamicos[remove_sc(dado)] = forms.DateField(required=dado.obrigatorio, label=remove_sc(dado), widget=admin.widgets.AdminDateWidget())
            elif dado.tipo == 'HR':
                campos_dinamicos[remove_sc(dado)] = forms.TimeField(required=dado.obrigatorio, label=remove_sc(dado), widget=admin.widgets.AdminTimeWidget())
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
                    campos_dinamicos[remove_sc(dado)] = forms.ChoiceField(required=dado.obrigatorio, choices=choices, label=remove_sc(dado), widget=forms.RadioSelect())
                else:
                    campos_dinamicos[remove_sc(dado)] = forms.MultipleChoiceField(required=dado.obrigatorio, choices=choices, label=remove_sc(dado), widget=forms.CheckboxSelectMultiple())
            else:
                campos_dinamicos[remove_sc(dado)] = forms.CharField(required=dado.obrigatorio, max_length=max_length, label=remove_sc(dado), widget=forms.TextInput(attrs={'class': 'vTextField'}))
        
        InscricaoFormDinamic = type('', (InscricaoForm,), campos_dinamicos)
        return InscricaoFormDinamic
    except:
        return InscricaoForm

def getInscricaoField(id_inscricao):
    fieldsets = [
                     ('Inscricao',             {'classes': ('collapse open',), 'fields': ('evento', 'tipo_inscricao', 'data')},),
        ]
    try:
        inscricao = Inscricao.objects.get(id=id_inscricao)
        dados = CampoTipoInscricao.objects.filter(tipo_inscricao=inscricao.tipo_inscricao).order_by('id')
        if dados:
            fieldset = ['Dados',]
            aux = {'classes': ('collapse open',), }
            aux['fields'] = []
            extra = []
            for dado in dados:
                if dado.tipo in ('SE', 'TE', 'CE', 'CF', 'CJ', 'NF', 'NI', 'DT', 'HR',):
                    if len(extra) <= 2:
                        extra.append(remove_sc(dado))
                    else:
                        aux['fields'].append(tuple(extra))
                        extra = []
                        extra.append(remove_sc(dado))
                else:
                    aux['fields'].append(remove_sc(dado))
            if len(extra): aux['fields'].append(tuple(extra))
            fieldset.append(aux)
            fieldsets.append(fieldset)
        return fieldsets
    except:
        return fieldsets



class AdminInscricao(admin.ModelAdmin):
    """
    ModelAdmin AdminInscricao, admin do modelo Inscricao
    """
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'js/ajax.js',
        )
        
    list_display = ('id', 'inscricao', 'evento', 'tipo_inscricao', 'usuario', 'data', 'acoes', )
    search_fields = ['evento__nome', 'tipo_inscricao__nome', ]
    list_filter = ('data', )
    readonly_fields = ('evento', 'tipo_inscricao', 'usuario', 'data',)
    form = InscricaoForm
    
    fieldsets = [
                     ('Inscricao',             {'classes': ('collapse open',), 'fields': ('evento', 'tipo_inscricao', 'data', )},),
        ]

    list_report = ('id', 'inscricao', 'evento', 'tipo_inscricao', 'usuario', 'data', )
    actions = [report_generic, make_certificado_inscricao, ]
    
    def inscricao(self, obj):
        try:
            dado = CampoTipoInscricao.objects.filter(tipo_inscricao=obj.tipo_inscricao).order_by('id')[0]
            return DadosInscricao.objects.get(inscricao=obj, campo=dado)
        except:
            return ''
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "evento":
                eventos = Evento.objects.filter(autor=request.user)
                kwargs["queryset"] = eventos
            elif db_field.name == "tipo_inscricao":
                tipo_inscricao = TipoInscricao.objects.filter(evento__autor=request.user)
                kwargs["queryset"] = tipo_inscricao
        return super(AdminInscricao, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def queryset(self, request):
        qs = super(AdminInscricao, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__autor=request.user)

    def change_view(self, request, object_id, extra_context=None):
        self.form = getInscricaoFormDinamic(object_id)
        self.fieldsets = getInscricaoField(object_id)
        self.save_on_top = True
        return super(AdminInscricao, self).change_view(request, object_id, extra_context)

    def save_model(self, request, obj, form, change):
        super(AdminInscricao, self).save_model(request, obj, form, change)
        if change:
            campos = CampoTipoInscricao.objects.filter(tipo_inscricao=obj.tipo_inscricao).order_by('id')
            for campo in campos:
                dado = DadosInscricao.objects.get(inscricao=obj, campo=campo)
                dado.resposta=form.cleaned_data[remove_sc(campo)]
                dado.save()

class AdminFonte(admin.ModelAdmin):
    """
    ModelAdmin AdminFonte, admin do modelo Fonte
    """
        
    list_display = ('nome', 'fonte',  'acoes',)
    search_fields = ['nome', 'fonte',]
    save_on_top = True

    fieldsets = [
        ('Fonte',             {'classes': ('collapse open',), 'fields': ('nome', 'fonte',)},),
       ]



       
class CampoCertificadoInline(admin.TabularInline):
    """
        TabularInline CamposInline, admin Inline do modelo Campo.
        Usado no ModelAdmin AdminCertificado
    """
    model = CampoCertificado
    form = CampoCertificadoForm
    classes = ('collapse open',)
    extra = 1
    allow_add = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "campo":
                try:
                    request_url = request.build_absolute_uri(request.get_full_path())
                    id = request_url.split("/")[-2]
                    certificado = Certificado.objects.get(id=id)
                    campos = CampoTipoInscricao.objects.filter(tipo_inscricao=certificado.tipo_inscricao)
                    kwargs["queryset"] = campos

                except:
                    pass
        return super(CampoCertificadoInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class AdminCertificado(admin.ModelAdmin):
    """
    ModelAdmin AdminCertificado, admin do modelo Certificado
    """
    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + 'js/ajax.js',
        )
        
    list_display = ('evento', 'tipo_inscricao', 'img_template', 'acoes', )
    search_fields = ['evento__nome',]
    inlines = [CampoCertificadoInline, ]
    form = CertificadoForm
    save_on_top = False
    change_form_template = 'admin/change_forward_form.html'
    
    fieldsets = [
        ('Certificado',             {'classes': ('collapse open',), 'fields': ('evento', 'tipo_inscricao', 'template',)},),
       ]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "evento":
                eventos = Evento.objects.filter(autor=request.user)
                kwargs["queryset"] = eventos
            elif db_field.name == "tipo_inscricao":
                tipo_inscricao = TipoInscricao.objects.filter(evento__autor=request.user)
                kwargs["queryset"] = tipo_inscricao
        return super(AdminCertificado, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def queryset(self, request):
        qs = super(AdminCertificado, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(evento__autor=request.user)

    def add_view(self, request, form_url="", extra_context=None):
        self.save_on_top = False
        return super(AdminCertificado, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        self.save_on_top = True
        return super(AdminCertificado, self).change_view(request, object_id, extra_context)
    
    
    
admin.site.register(Evento, AdminEvento)
admin.site.register(Realizacao, AdminRealizacao)
admin.site.register(Apoio, AdminApoio)
admin.site.register(Apresentador, AdminApresentador)
admin.site.register(Apresentacao, AdminApresentacao)
admin.site.register(TipoInscricao, AdminTipoInscricao)
admin.site.register(Inscricao, AdminInscricao)
admin.site.register(Fonte, AdminFonte)
admin.site.register(Certificado, AdminCertificado)