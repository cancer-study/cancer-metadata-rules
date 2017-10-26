from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES

from edc_metadata_rules import PredicateCollection


class Predicates(PredicateCollection):

    app_label = 'cancer_subject'
    visit_model = f'{app_label}.subjectvisit'
