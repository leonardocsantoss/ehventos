from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #Ajax
    url(r'^get/all/$', 'ehv.views.all', name="ehv_all"),
    url(r'^get/tipoinscricao/(?P<evento_id>\d+)/$', 'ehv.views.getTipoInscao', name="gettipoinscricao"),
    url(r'^(?P<slug>[\w_-]+)/$', 'ehv.views.evento', name="getevento"),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', 'ehv.views.inscricao', name="ehv_inscricao"),
    

)