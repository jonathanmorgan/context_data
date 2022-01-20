from __future__ import unicode_literals

from django.apps import AppConfig

class ContextDataConfig(AppConfig):

    name = 'context_data'

    default_auto_field = 'django.db.models.AutoField'
    # if you have lots of rows:
    # default_auto_field = 'django.db.models.BigAutoField'

#-- END class ContextDataConfig --#
