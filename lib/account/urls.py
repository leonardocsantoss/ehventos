# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^registro/$', 'account.views.signup', name="acct_signup"),
    url(r'^entrar/$', 'account.views.login', name="acct_login"),
    url(r'^alterar/senha/$', 'account.views.password_change', name="acct_passwd"),
    url(r'^criar/senha/$', 'account.views.password_set', name="acct_passwd_set"),
    url(r'^deletar/senha/$', 'account.views.password_delete', name="acct_passwd_delete"),
    url(r'^deletar/senha/deletada/$', 'django.views.generic.simple.direct_to_template', {
        "template": "account/password_delete_done.html",
    }, name="acct_passwd_delete_done"),
    url(r'^redefinir/senha/$', 'account.views.password_reset', name="acct_passwd_reset"),
    
    url(r'^linguagem/$', 'account.views.language_change', name="acct_language_change"),
    url(r'^sair/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name="acct_logout"),
    
    url(r'^confirmar/email/(\w+)/$', 'emailconfirmation.views.confirm_email', name="acct_confirm_email"),

    # Setting the permanent password after getting a key by email
    url(r'^alerar/senha/key/(\w+)/$', 'account.views.password_reset_from_key', name="acct_passwd_reset_key"),

)
