# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime, date
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from django.contrib.admin.models import User
from filebrowser.fields import FileBrowseField

from tagging_autocomplete.models import TagAutocompleteField
from utils.widgets import AddressField
from django.core.urlresolvers import reverse


TIPO_APRESENTACAO = (
    ('P', u'Palestra'),
    ('M', u'Mini-curso'),
    ('S', u'Seminário'),
    ('W', u'Workshop'),
    ('R', u'Mesa-redonda')
        
)

TIPO_CAMPO = (
    ('', u'--------'),
    ('TX', u'Texto'),
    ('EM', u'Email'),
    ('SE', u'Senha'),
    ('TE', u'Telefone'),
    ('ES', u'Escolha'),
    ('ME', u'Múltipla Escolha'),
    ('CE', u'CEP'),
    ('CF', u'CPF'),
    ('CJ', u'CNPJ'),
    ('NF', u'Número'),
    ('NI', u'Número inteiro'),
    ('DT', u'Data'),
    ('HR', u'Hora'),
)

TIPO_LETRA = (
        ('MA', 'Maiuscula'),
        ('N', 'Normal'),
)

COR_CHOICES = (
    ("#000000", u"Preto"),
    ("#FFFFFF", u"Branco"),
    ("#808080", u"Cinza"),
    ("#C0C0C0", u"Prateado"),
    ("#0000FF", u"Azul"),
    ("#008080", u"Azul-petróleo"),
    ("#000080", u"Azul-marinho"),
    ("#00FFFF", u"Azul-piscina"),
    ("#FFFF00", u"Amarelo"),
    ("#FFFFE0", u"Amarelo claro"),
    ("#FFD700", u"Dourado"),
    ("#008000", u"Verde"),
    ("#808000", u"Verde-oliva"),
    ("#00FF00", u"Verde-limão"),
    ("#FF0000", u"Vermelho"),
    ("#FF00FF", u"Rosa"),
    ("#FF69B4", u"Rosa quente"),
    ("#800080", u"Roxo"),
    ("#EE82EE", u"Violeta"),
)

class Evento(models.Model):
    """
        Modelo evento, onde contém as informações do evento.
    """
    
    autor = models.ForeignKey(User)
    logomarca = FileBrowseField(max_length=200, format='Image', verbose_name=u'Logomarca', help_text=u'Selecione a logomarca do evento.')
    nome = models.CharField(max_length=255, unique=True, verbose_name=u'Nome do evento', help_text=u'Digite o nome do evento.')
    slug = models.SlugField(blank=True, unique=True)
    descricao = models.TextField(help_text=u'Digite a descricao do evento.')
    tags = TagAutocompleteField(verbose_name=u'Tags', help_text=u'Digite uma descrição em tags para o evento.')

    class Meta:
        ordering = ('id',)
        verbose_name = _(u'1º - Evento')
        verbose_name_plural = _(u'1º - Eventos')    
        
    def __unicode__(self):
        return u'%s' % self.nome

    def get_absolute_url(self):
        return reverse('ehv.views.evento',kwargs={'slug': self.slug})

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_generic_detailed'); $('#list_form').submit(); })(jQuery);\" >Imprimir</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"

    def aberta(self):
        for tipo_inscricao in TipoInscricao.objects.filter(evento=self):
            if tipo_inscricao.aberta():
                return True
        return False
    
    def logo(self):
        if self.logomarca:
            return '<img src="%s" />' % self.logomarca.url_thumbnail
        else:
            return ""
    logo.allow_tags = True

def evento_pre_save(signal, instance, sender, **kwargs):
    """
        Este signal gera um slug automaticamente.
    """
    if not instance.slug:
        instance.slug = slugify(instance.nome)
signals.pre_save.connect(evento_pre_save, sender=Evento)


class Realizacao(models.Model):
    """
        Modelo realização, onde contém as informações da realização do evento.
        Uma realização está associado a um evento.
    """
    evento = models.ForeignKey(Evento, verbose_name=_(u'Evento'), help_text=u'Selecione o evento.')
    nome = models.CharField(max_length=255, verbose_name=u'Nome da realização', help_text=u'Digite o nome da realização.')
    link = models.URLField(blank=True, null=True, verbose_name=u'Link da realização', help_text=u'Digite o link da realização.')
    logomarca = FileBrowseField(max_length=200, format='Image', verbose_name=u'Logomarca', help_text=u'Selecione a logomarca da realização.')

    class Meta:
        ordering = ('id',)
        verbose_name = _(u'2º - Realização')
        verbose_name_plural = _(u'2º - Realizações')    

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_generic_detailed'); $('#list_form').submit(); })(jQuery);\" >Imprimir</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.evento)

    def logo(self):
        if self.logomarca:
            return '<img src="%s" />' % self.logomarca.url_thumbnail
        else:
            return ""
    logo.allow_tags = True


class Apoio(models.Model):
    """
        Modelo apoio, onde contém as informações do apoio.
        Um apoio está associado a um evento.
    """
    evento = models.ForeignKey(Evento, verbose_name=u'Evento', help_text=u'Selecione o evento.')
    nome = models.CharField(max_length=255, verbose_name=u'Nome do apoio', help_text=u'Digite o nome do apoio.')
    link = models.URLField(blank=True, null=True, verbose_name=u'Link do apoio', help_text=u'Digite o link do apoio.')
    logomarca = FileBrowseField(max_length=200, format='Image', verbose_name=u'Logomarca', help_text=u'Selecione a logomarca do apoio.')

    class Meta:
        ordering = ('id',)
        verbose_name = _(u'3º - Apoio')
        verbose_name_plural = _(u'3º - Apoios')    

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_generic_detailed'); $('#list_form').submit(); })(jQuery);\" >Imprimir</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.evento)

    def logo(self):
        if self.logomarca:
            return '<img src="%s" />' % self.logomarca.url_thumbnail
        else:
            return ""
    logo.allow_tags = True
    
    

class Apresentador(models.Model):
    """
        Modelo apresentador, onde contém as informações referente aos apresentadores.
        O modelo está associado a uma ou mais apresentação.
    """
    autor = models.ForeignKey(User)
    nome = models.CharField(max_length=255, verbose_name=u'Nome completo', help_text=u'Digite o nome do apresentador.')
    email = models.EmailField(max_length=255, verbose_name=u'Email', help_text=u'Digite o email do apresentador.')
    link = models.URLField(blank=True, null=True, verbose_name=u'Link', help_text=u'Digite o link da realização.')
    descricao = models.TextField(verbose_name=u'Descricao', help_text=u'Digite uma descrição para o apresentador.')
    tags = TagAutocompleteField(verbose_name=u'Tags', help_text=u'Digite uma descrição em tags para o apresentador.')
    
    class Meta:
        ordering = ('id',)
        verbose_name = _(u'4º - Apresentador')
        verbose_name_plural = _(u'4º - Apresentadores')    

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_generic_detailed'); $('#list_form').submit(); })(jQuery);\" >Imprimir</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.email)

    def foto_apresentador(self):
        try:
           import hashlib.md5 as md5
        except ImportError:
           import md5 as md5
        gravatar = "http://www.gravatar.com/avatar/" + md5.md5(self.email.lower()).hexdigest() + "?s=80"
        return '<img src="%s" />' % gravatar
    foto_apresentador.allow_tags = True
    

class Apresentacao(models.Model):
    """
        Modelo apresentação, onde contém as informações referentas as apresentações do evento.
        O modelo está associado ao evento e contém uma lista de apresentadores.
    """
    titulo = models.CharField(max_length=255, verbose_name=u'Titulo da apresentação', help_text=u'Digite titulo da apresentação.')
    tipo = models.CharField(max_length=1, choices=TIPO_APRESENTACAO, verbose_name=u'Tipo da apresentação', help_text=u'Selecione o tipo da apresentação.')
    evento = models.ForeignKey(Evento, verbose_name=u'Evento', help_text=u'Selecione o evento.')
    apresentadores = models.ManyToManyField(Apresentador, verbose_name='Apresentador', help_text='Selecione o apresentador da apresentação.')
    local = AddressField(blank=True, max_length=255)
    descricao = models.TextField(verbose_name=u'Descrição da apresentação', help_text=u'Digite uma descrições para a apresentação.')
    tags = TagAutocompleteField(verbose_name=u'Tags', help_text=u'Digite uma descrição em tags para a apresentação.')
    
    class Meta:
        ordering = ('id',)
        verbose_name = _(u'5º - Apresentação')
        verbose_name_plural = _(u'5º - Apresentações')    

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_generic_detailed'); $('#list_form').submit(); })(jQuery);\" >Imprimir</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def __unicode__(self):
        return u'%s - %s' % (self.titulo, self.evento)



class DataHora(models.Model):
    """
        Modelo DataHora, onde contém uma data e uma hora associada a uma apresentação.
    """
    apresentacao = models.ForeignKey(Apresentacao)
    data_hora = models.DateTimeField(verbose_name=u'Data/Hora', help_text=u'Selecione a(s) data(s)/hora(s) da apressentação.')

    class Meta:
        ordering = ('data_hora',)
        verbose_name = _(u'Data/Hora da apresentação')
        verbose_name_plural = _(u'Datas/Horas da apresentação')
        
    def __unicode__(self):
        return u'%s - %s' % (self.data_hora, self.apresentacao)

    
    
    
class TipoInscricao(models.Model):
    """
        Modelo tipoInscricao, onde contém imformações referentes aos tipos de inscrições que podemos criar.
        O modelo está associado a um evento, e contém uma lista de apresentações.
    """
    nome = models.CharField(max_length=255, verbose_name=u'Nome', help_text=u'Digite o nome do tipo de inscriação.')
    evento = models.ForeignKey(Evento, verbose_name=u'Evento', help_text=u'Selecione o evento a qual esse tipo de inscrição pertence.')
    vagas = models.PositiveIntegerField(verbose_name=u'Numeros de vagas', help_text=u'Informe o números de vagas.')
    publicado = models.BooleanField(default=True, verbose_name=u'Publicado', help_text=u'Marque se esse tipo de inscrição está publicado.')
    data_inicio_inscricao = models.DateField( verbose_name=u'Data de inicio', help_text=u'Data de início das inscrições.')
    data_fim_inscricao = models.DateField(verbose_name=u'Data de fim', help_text=u'Data do fim das inscrições.')
    apresentacoes = models.ManyToManyField(Apresentacao, verbose_name=u'Apresentações', help_text=u'Selecione as apresentações referentes a esse tipo de inscrição.')
    
    class Meta:
        ordering = ('id', )
        verbose_name = _(u'6º - Tipo de inscrição')
        verbose_name_plural = _(u'6º - Tipos de inscrições')

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_generic_detailed'); $('#list_form').submit(); })(jQuery);\" >Imprimir</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'report_list'); $('#list_form').submit(); })(jQuery);\" >Lista de presença</a></li>" % (self.pk, )
        a4 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'make_certificado_tipo'); $('#list_form').submit(); })(jQuery);\" >Gerar certificados</a></li>" % (self.pk, )
        a5 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+a4+a5+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def vagas_abertas(self):
        return self.vagas - Inscricao.objects.filter(tipo_inscricao=self).count()

    def aberta(self):
        if self.publicado and date.today() >= self.data_inicio_inscricao and date.today() <= self.data_fim_inscricao and self.vagas_abertas() > 0:
            return True
        else:
            return False

    def estou_inscrito(self, usuario):
        try:
            Inscricao.objects.get(tipo_inscricao=self, usuario=usuario)
            return True
        except:
            return False
        
    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.evento)



class CampoTipoInscricao(models.Model):
    """
        Modelo campoTipoInscricao, onde contém imformações referentes aos campos dos tipos de inscrições que podemos criar.
        O modelo está associado a um tipoInscrição, e contém o tipo do campo.
    """
    tipo_inscricao = models.ForeignKey(TipoInscricao)
    nome = models.CharField(max_length=30, verbose_name=u'Nome do campo', help_text=u'Digite o nome do campo da inscrição.')
    obrigatorio = models.BooleanField(default=True, verbose_name=u'Campo obrigatório', help_text=u'Marque se esse campo for obrigatório.')
    tipo = models.CharField(max_length=2, choices=TIPO_CAMPO, verbose_name=u'Tipo do campo', help_text=u'Selecione o tipo do campo da inscrição.')
    
    class Meta:
        ordering = ('id', )
        verbose_name = _(u'Campo desse tipo de inscrição')
        verbose_name_plural = _(u'Campos desse tipo de inscrição')
        
    def __unicode__(self):
        return u'%s' %(self.nome)
    


class TipoTexto(models.Model):
    """
        Modelo tipoTexto, onde contém o tamanho do campo do tipo texto.
    """
    campo_tipo_inscricao = models.ForeignKey(CampoTipoInscricao)
    tamanho = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=u'Tamanho do campo', help_text=u'Digite o tamanho do campo da inscrição.')
    
    class Meta:
        ordering = ('id', )
        verbose_name = _(u'Campo do tipo texto')
        verbose_name_plural = _(u'Campos dos tipo texto')
        
    def __unicode__(self):
        return u'%s(%s)' %(self.campo_tipo_inscricao, self.tamanho)
    


class TipoAlternativa(models.Model):
    """
        Modelo tipoAlternativa, onde contém a alternativa do campo do tipo alternativa.
    """
    campo_tipo_inscricao = models.ForeignKey(CampoTipoInscricao)
    numero = models.SmallIntegerField()
    alternativa = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Alternativa do campo', help_text=u'Digite a alternativa do campo da inscrição.')
    
    class Meta:
        ordering = ('id', )
        verbose_name = _(u'Campo do tipo alternativa')
        verbose_name_plural = _(u'Campos dos tipo alternativa')
        
    def __unicode__(self):
        return u'%s(%s)' %(self.campo_tipo_inscricao, self.alternativa)



class Certificado(models.Model):
    """
        Modelo certificado, onde contém as informações do certificado.
    """
    class Meta:
        ordering = ('id',)
        unique_together = (("evento", "tipo_inscricao"),)
        verbose_name = u'7º - Certificado'
        verbose_name_plural = u'7º - Certificados'

    evento = models.ForeignKey(Evento, verbose_name='Evento', help_text=u'Selecione o evento.')
    tipo_inscricao = models.ForeignKey(TipoInscricao, verbose_name=u'Tipo de inscrição', help_text=u'Selecione o tipo de inscrição.')
    template = FileBrowseField(max_length=200, format='Image', verbose_name=u'Template', help_text=u'Selecione o template do certificado.')

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def __unicode__(self):
        return u'%s - %s' % (self.evento, self.tipo_inscricao)
    
    def img_template(self):
        if self.template:
            return '<img src="%s" />' % self.template.url_thumbnail
        else:
            return ""
    img_template.allow_tags = True


class Fonte(models.Model):
    """
        Modelo fonte, onde contém as informações das fontes.
    """
    class Meta:
        ordering = ('id',)
        verbose_name = _(u'Fonte')
        verbose_name_plural = _(u'Fontes')
        
    nome = models.CharField(max_length=30, verbose_name=u'Nome da fonte', help_text=u'Digite o nome da fonte.')
    fonte = FileBrowseField(max_length=200, format='Font', verbose_name=u'Fonte', help_text=u'Selecione a fonte.')

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"
    
    def __unicode__(self):
        return u'%s' %(self.nome)



class CampoCertificado(models.Model):
    """
        Modelo campoCertificado, onde contém as informações dos campos dos certificados.
    """
    class Meta:
        ordering = ('id',)
        verbose_name = _(u'Campo do certificado')
        verbose_name_plural = _(u'Campos do certificado')
        
    certificado = models.ForeignKey(Certificado)
    campo = models.ForeignKey(CampoTipoInscricao, verbose_name=u'Campo a ser rederizado', help_text=u'Selecione o campo de inscricao deste campo do certificado.')
    x = models.IntegerField(help_text=u'Digite a coordenada x deste campo do template do certificado.')
    y = models.IntegerField(help_text=u'Digite a coordenada y deste campo do template do certificado.')
    fonte = models.ForeignKey(Fonte, verbose_name=u'Fonte', help_text=u'Selecione a fonte deste campo do certificado.')
    cor = models.CharField(max_length=7, choices=COR_CHOICES, verbose_name=u'Cor', help_text=u'Selecione a cor da fonte deste campo do certificado.')
    tamanho = models.PositiveIntegerField(verbose_name=u'Tamanho da letra', help_text=u'Digite o tamanho da letra deste campo do certificado.')
    tipo = models.CharField(max_length=2, choices=TIPO_LETRA, verbose_name=u'Tipo da letra', help_text=u'Selecione o tipo da letra deste campo do certificado.')
    
    def __unicode__(self):
        return u'%s - %s' %(self.certificado, self.campo)



class Inscricao(models.Model):
        
    class Meta:
        ordering = ('id',)
        verbose_name = u'Inscrição'
        verbose_name_plural = 'Inscrições'

    usuario = models.ForeignKey(User, verbose_name='Usuário', help_text=u'Selecione o usuário da inscrição.')
    evento = models.ForeignKey(Evento, verbose_name='Evento', help_text=u'Selecione o evento da inscrição.')
    tipo_inscricao = models.ForeignKey(TipoInscricao, verbose_name=u'Tipo de inscrição', help_text=u'Selecione o tipo de inscrição.')
    data = models.DateTimeField(default=datetime.now, verbose_name=u'Data da inscrição', help_text=u'Selecione a Data da inscrição.')

    def acoes(self):
        a1 = u"<li style=\"margin-right: 10px;\"><a href=\"%s\" class=\"button\" style=\"padding-left: 7px;\" >Editar</a></li>" % (self.pk, )
        a2 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'make_certificado_inscricao'); $('#list_form').submit(); })(jQuery);\" >Gerar certificado</a></li>" % (self.pk, )
        a3 = u"<li style=\"margin-right: 10px;\"><a class=\"button\" style=\"padding-left: 7px;\" href=\"javascript://\" onClick=\"(function($) { $('input:checkbox[name=_selected_action]').attr('checked', ''); $('input:checkbox[name=_selected_action][value=%s]').attr('checked', 'checked'); $('select[name=action]').attr('value', 'delete_selected'); $('#list_form').submit(); })(jQuery);\" >Remover</a></li>" % (self.pk, )
        return "<ul class=\"actions\">"+a1+a2+a3+"</ul>"
    acoes.allow_tags = True
    acoes.short_description = u"Ações"

    def nome(self):
        return "%s %s" % (self.usuario.first_name, self.usuario.last_name)

    def assinatura(self):
        return "___________________________________________________"
    
    def __unicode__(self):
        return u'%s - %s' %(self.evento, self.tipo_inscricao)
    
    
    
class DadosInscricao(models.Model):
    
    class Meta:
        ordering = ('id',)
        
    inscricao = models.ForeignKey(Inscricao, verbose_name=u'Inscrição', help_text=u'Selecione a inscrição do Dado.')
    campo = models.ForeignKey(CampoTipoInscricao, verbose_name=u'Campo', help_text=u'Selecione a campo do Dado.')
    resposta = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Resposta', help_text=u'Digite a resposta do Dado.')
    
    def __unicode__(self):
        return u'%s' % self.resposta