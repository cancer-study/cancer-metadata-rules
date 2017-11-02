from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'cancer_metadata_rules'


if settings.APP_NAME == 'cancer_metadata_rules':
    from edc_metadata.apps import AppConfig as MetadataAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig

    class EdcMetadataAppConfig(MetadataAppConfig):
        reason_field = {'cancer_metadata_rules.subjectvisit': 'reason'}

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'cancer_subject': ('subject_visit', 'cancer_subject.subjectvisit')}
