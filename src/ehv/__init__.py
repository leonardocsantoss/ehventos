from django.db.models import signals
from django.contrib.admin.models import User
import os
from django.conf import settings
from filebrowser.settings import DIRECTORY

def user_mkdir_pre_save(signal, instance, sender, **kwargs):
    """
        Este signal gera uma pasta com o nome do usuario dentro da pasta de upload.
    """
    path = os.path.join(settings.MEDIA_ROOT, DIRECTORY, str(instance.username))
    
    if not os.path.exists(path):
        os.mkdir(path)
        os.chmod(path, 0775)
signals.pre_save.connect(user_mkdir_pre_save, sender=User)


def user_mkdir_pre_delete(signal, instance, sender, **kwargs):
    """
        Este signal deleta a pasta com o nome do usuario dentro da pasta de upload.
    """
    path = os.path.join(settings.MEDIA_ROOT, DIRECTORY, str(instance.username))
    
    if os.path.exists(path):
        os.removedirs(path)
signals.pre_delete.connect(user_mkdir_pre_delete, sender=User)
