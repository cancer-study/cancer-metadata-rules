from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES

from edc_metadata_rules import PredicateCollection


class Predicates(PredicateCollection):

    app_label = 'cancer_subject'
    visit_model = f'{app_label}.subjectvisit'

    @property
    def base_risk_assessment_smoking_model_cls(self):
        return django_apps.get_model(f'{self.app_label}.baseriskassessmentsmoking')

    @property
    def base_risk_assessment_model_cls(self):
        return django_apps.get_model(f'{self.app_label}.baseriskassessment')

    def func_oncology_plan(self, visit, **kwargs):
        try:
            model_cls = self.get_model('oncologytreatmentplan')
            model_cls.objects.get(subject_visit=visit, radiation_plan=YES)
        except model_cls.DoesNotExist:
            return False
        return True
