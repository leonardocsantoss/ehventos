# -*- coding:utf-8 -*-
import os

from django import forms

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.db import models
from django.conf import settings

# django imports
from django.utils.encoding import force_unicode
# filebrowser imports
from filebrowser.settings import *


class MyDateWidget(forms.DateInput):

    format = '%d/%m/%Y'

    def __init__(self, attrs=None):
        super(MyDateWidget, self).__init__(attrs=attrs)

    def render(self, name, value=None, attrs=None):
        if value == None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        output = [u"""  <script type="text/javascript">
                            jQuery(function($){
                               $("#%s").mask("99/99/9999");
                            });
                        </script>""" % force_unicode(final_attrs['id'])]
        output.append(u'<input%s value="%s"/>' %(flatatt(final_attrs), force_unicode(value)))
        return mark_safe(u'\n'.join(output))



class Readonly(forms.TextInput):
    input_type = 'hidden'
    """
        Widget de leitura para campos select.
        É necessário passar o modelo na inicialização.
    """

    def __init__(self, model=None, choices=None, attrs=None):
        super(Readonly, self).__init__(attrs=attrs)
        self.model = model
        self.choices = choices


    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs_div = self.build_attrs(attrs)
        output = [u'<style type="text/css"> #add_id_%s { display: none; }</style>' % (force_unicode(name))]
        if value != '':
            if self.model is not None:
                output.append(u'<div%s>%s</div><input%s value="%s">' % (flatatt(final_attrs_div), force_unicode(self.model.objects.get(pk=value)), flatatt(final_attrs), force_unicode(value)))
            else:
                if self.choices is not None:
                    output.append(self.rende_choices(value, final_attrs_div, final_attrs))
                else:
                    output.append(u'<div%s>%s</div><input%s value="%s">' % (flatatt(final_attrs_div), force_unicode(value), flatatt(final_attrs), force_unicode(value)))
        else:
            output.append(u'<div%s></div><input%s value="">' %(flatatt(final_attrs_div), flatatt(final_attrs)))
        return mark_safe(u'\n'.join(output))

    def rende_choices(self, value, final_attrs_div, final_attrs):
        for val, retorno in self.choices:
            if val == value:
                return u'<div%s>%s</div><input%s value="%s">' % (flatatt(final_attrs_div), force_unicode(retorno), flatatt(final_attrs), force_unicode(value))

class MyCPFWidget(forms.TextInput):

    def __init__(self, attrs=None):
        super(MyCPFWidget, self).__init__(attrs=attrs)

    def render(self, name, value=None, attrs=None):
        if value == None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        output = [u"""  <script type="text/javascript">
                            jQuery(function($){
                               $("#%s").mask("999.999.999-99");
                            });
                        </script>""" % force_unicode(final_attrs['id'])]
        output.append(u'<input%s value="%s"/>' %(flatatt(final_attrs), force_unicode(value)))
        return mark_safe(u'\n'.join(output))



class MyCNPJWidget(forms.TextInput):

    def __init__(self, attrs=None):
        super(MyCNPJWidget, self).__init__(attrs=attrs)

    def render(self, name, value=None, attrs=None):
        if value == None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        output = [u"""  <script type="text/javascript">
                            jQuery(function($){
                               $("#%s").mask("99.999.999/9999-99");
                            });
                        </script>""" % force_unicode(final_attrs['id'])]
        output.append(u'<input%s value="%s"/>' %(flatatt(final_attrs), force_unicode(value)))
        return mark_safe(u'\n'.join(output))


class MyTelefoneWidget(forms.TextInput):

    def __init__(self, attrs=None):
        super(MyTelefoneWidget, self).__init__(attrs=attrs)

    def render(self, name, value=None, attrs=None):
        if value == None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        output = [u"""  <script type="text/javascript">
                            jQuery(function($){
                               $("#%s").mask("99-9999-9999");
                            });
                        </script>""" % force_unicode(final_attrs['id'])]
        output.append(u'<input%s value="%s"/>' %(flatatt(final_attrs), force_unicode(value)))
        return mark_safe(u'\n'.join(output))


class MyCEPWidget(forms.TextInput):

    def __init__(self, attrs=None):
        super(MyCEPWidget, self).__init__(attrs=attrs)

    def render(self, name, value=None, attrs=None):
        if value == None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        output = [u"""  <script type="text/javascript">
                            jQuery(function($){
                               $("#%s").mask("99999-999");
                            });
                        </script>""" % force_unicode(final_attrs['id'])]
        output.append(u'<input%s value="%s"/>' %(flatatt(final_attrs), force_unicode(value)))
        return mark_safe(u'\n'.join(output))


class AddressWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.MEDIA_URL + 'address/css/address.css',
            )
        }
        js = (
            settings.MEDIA_URL + 'admin/jquery/jquery-1.4.2.min.js',
            'http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAd7Q5mN9809jSpiJV3vlNqBQO3kU2fVtsM_YKb6Sepb25TCvIEBQEHRP9vAfLlD6LaViG00sfVoEDmw',
            settings.MEDIA_URL + 'address/js/address.js',
        )

    def __init__(self, attrs=None):
        super(AddressWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if attrs is None: attrs = {}
        attrs['class'] = 'location vTextField'
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        output = [u'<input type="text"%s value="%s">' % (flatatt(final_attrs), force_unicode(value))]
        output.append('<input type="button" class="go" value="Pesquisar"/><div id="map_canvas"</div>')
        return mark_safe(u'\n'.join(output))



class AddressField(models.CharField):

    def formfield(self, **kwargs):
        kwargs['widget'] = AddressWidget
        return super(AddressField, self).formfield(**kwargs)



class CertificadoFileBrowseWidget(forms.widgets.Input):
    input_type = 'text'

    class Media:
        js = (os.path.join(URL_FILEBROWSER_MEDIA, 'js/AddFileBrowser.js'), )

    def __init__(self, attrs=None):
        self.directory = attrs.get('directory', '')
        self.extensions = attrs.get('extensions', '')
        self.format = attrs.get('format', '')
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['search_icon'] = URL_FILEBROWSER_MEDIA + 'img/filebrowser_icon_show.gif'
        final_attrs['directory'] = self.directory
        final_attrs['extensions'] = self.extensions
        final_attrs['format'] = self.format
        final_attrs['TEMPLATE_CERTIFICADO'] = TEMPLATE_CERTIFICADO
        final_attrs['DEBUG'] = DEBUG
        if value != "":
            try:
                final_attrs['directory'] = os.path.split(value.path_relative_directory)[0]
            except:
                pass
        return render_to_string("ehv/custom_field_certificado.html", locals())