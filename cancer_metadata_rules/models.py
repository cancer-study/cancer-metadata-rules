from django.conf import settings

if settings.APP_NAME == 'cancer_metadata_rules':
    from .tests import models
