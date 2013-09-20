# -*- coding: utf-8 -*-
from report.html2report import html_report_generic
from django.http import HttpResponse
from django.conf import settings
import ho.pisa as pisa
from cStringIO import StringIO
import zipfile
import os
from django.utils.encoding import smart_str
from models import Inscricao, Certificado, CampoCertificado, DadosInscricao
from PIL import ImageDraw, Image, ImageFont
from filebrowser.functions import get_version_path
from django.utils.encoding import smart_str

def remove_sc(txt, codif='utf-8'):
    from unicodedata import normalize
    return normalize('NFKD', smart_str(txt).decode(codif)).encode('ASCII','ignore').replace(" ", "_")

def report_list(self, request, queryset):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % smart_str("Lista_de_presenca")

    html = html_report_generic(u"<h1>Lista de presença</h1>", ("evento", "tipo_inscricao", "nome", "assinatura", ), Inscricao.objects.filter(tipo_inscricao=queryset[0]) )
    pdf = pisa.CreatePDF(html, response)

    return response

report_list.short_description = u"Imprimir lista de preseça"


def make_certificado_tipo(self, request, queryset):

    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'filename=Certificados.zip'

    buffer = StringIO()
    zip = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED)

    try:
        certificado = Certificado.objects.get(tipo_inscricao=queryset[0])
    except:
        self.message_user(request, u'Ainda não há um certificado cadastrado para esse tipo de inscrição!')
        return
    campos = CampoCertificado.objects.filter(certificado=certificado)

    inscricoes = Inscricao.objects.filter(tipo_inscricao=queryset[0])
    for inscricao in inscricoes:
        template = Image.open(settings.MEDIA_ROOT+"/"+get_version_path(certificado.template.path, 'template_certificado'))
        draw = ImageDraw.Draw(template)

        for campo in campos:
            try:
                texto =  DadosInscricao.objects.get(inscricao=inscricao, campo=campo.campo).resposta
            except:
                self.message_user(request, 'Erro! Verifique se o campo \"'+str(campo.campo)+'\" da Inscrição Nº '+str(inscricao.id)+' foi preenchido!')
                return
            if campo.tipo == 'MA':
                texto = texto.upper()
            posicao = campo.x, (campo.y-campo.tamanho)-campo.tamanho/2
            fonte = ImageFont.truetype(settings.MEDIA_ROOT+"/"+campo.fonte.fonte.path, campo.tamanho)
            draw.text(posicao, texto, font=fonte, fill=campo.cor)

        if campos:
            local = settings.MEDIA_ROOT+'/certificados/tmp/'

            nome =  remove_sc(str(inscricao.evento))+' - '+remove_sc(str(queryset[0]))+' - '+remove_sc(DadosInscricao.objects.filter(inscricao=inscricao)[0].resposta)+'.png'

            template.save(local+nome)
            zip.write(local+nome, nome)
            os.remove(local+nome)
        else:
            self.message_user(request, u'Erro! Verifique se há certificados sem campos e/ou tipos de inscrições sem dados cadastrais!')
            return

    zip.close()
    buffer.flush()
    ret_zip = buffer.getvalue()
    buffer.close()
    response.write(ret_zip)
    return response

make_certificado_tipo.short_description = "Gerar certificados"



def make_certificado_inscricao(self, request, queryset):

    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'filename=Certificados.zip'

    buffer = StringIO()
    zip = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED)

    try:
        certificado = Certificado.objects.get(tipo_inscricao=queryset[0].tipo_inscricao)
    except:
        self.message_user(request, u'Ainda não há um certificado cadastrado para esse tipo de inscrição!')
        return
    campos = CampoCertificado.objects.filter(certificado=certificado)

    inscricoes = queryset
    for inscricao in inscricoes:
        template = Image.open(settings.MEDIA_ROOT+"/"+get_version_path(certificado.template.path, 'template_certificado'))
        draw = ImageDraw.Draw(template)

        for campo in campos:
            try:
                texto =  DadosInscricao.objects.get(inscricao=inscricao, campo=campo.campo).resposta
            except:
                self.message_user(request, 'Erro! Verifique se o campo \"'+str(campo.campo)+'\" da Inscrição Nº '+str(inscricao.id)+' foi preenchido!')
                return
            if campo.tipo == 'MA':
                texto = texto.upper()
            posicao = campo.x, (campo.y-campo.tamanho)-campo.tamanho/2
            fonte = ImageFont.truetype(settings.MEDIA_ROOT+"/"+campo.fonte.fonte.path, campo.tamanho)
            draw.text(posicao, texto, font=fonte, fill=campo.cor)

        if campos:
            local = settings.MEDIA_ROOT+'/certificados/tmp/'

            nome =  remove_sc(str(inscricao.evento))+' - '+remove_sc(str(queryset[0].tipo_inscricao))+' - '+remove_sc(DadosInscricao.objects.filter(inscricao=inscricao)[0].resposta)+'.png'

            template.save(local+nome)
            zip.write(local+nome, nome)
            os.remove(local+nome)
        else:
            self.message_user(request, u'Erro! Verifique se há certificados sem campos e/ou tipos de inscrições sem dados cadastrais!')
            return

    zip.close()
    buffer.flush()
    ret_zip = buffer.getvalue()
    buffer.close()
    response.write(ret_zip)
    return response

make_certificado_inscricao.short_description = "Gerar certificados"