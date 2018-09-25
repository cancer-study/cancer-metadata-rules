from django.apps import apps as django_apps

from edc_metadata_rules import PredicateCollection
from edc_constants.constants import YES, POS


class Predicates(PredicateCollection):

    app_label = 'cancer_subject'
    visit_model = f'{app_label}.subjectvisit'

    def func_oncology_plan(self, visit=None, **kwargs):
        values = self.exists(
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name='radiation_plan')
        return values[0] == YES

    def func_oncology_record(self, visit=None, **kwargs):
        values = self.exists(
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name='radiation_received')
        return values[0] == YES

    def func_oncology(self, visit=None, **kwargs):
        show_radiation_treatment = False
        if self.func_oncology_plan(visit) and self.func_oncology_record(visit):
            show_radiation_treatment = True
        elif not self.func_oncology_plan(visit) and self.func_oncology_record(visit):
            show_radiation_treatment = True
        elif self.func_oncology_plan(visit) and not self.func_oncology_record(visit):
            show_radiation_treatment = True
        elif not self.func_oncology_plan(visit) and not self.func_oncology_record(visit):
            show_radiation_treatment = False
        return show_radiation_treatment

    def func_haematology(self, visit=None, **kwargs):
        haematology = django_apps.get_model(
            f'{self.app_label}.resultstorecord')
        result_to_record = haematology.objects.get(
            name='haematology')
        model_cls = f'{self.app_label}.cancerdiagnosis'
        try:
            model_cls.objects.get(
                subject_visit=visit, results_to_record__in=[haematology])
        except model_cls.DoesNotExist:
            return False
        return True

    def func_chemistry(self, visit=None, **kwargs):
        values = self.exists(
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name='radiation_received')
        return values[0] == YES

        chemistry = f'{self.app_label}.resultstorecord'.objects.get(
            name='chemistry')
        model_cls = f'{self.app_label}.cancerdiagnosis'
        try:
            model_cls.objects.get(
                subject_visit=visit, results_to_record__in=[chemistry])
        except model_cls.DoesNotExist:
            return False
        return True

    def func_tubercolosis(self, visit=None, **kwargs):
        tb = f'{self.app_label}.resultstorecord'.objects.get(
            name='tubercolosis')
        model_cls = f'{self.app_label}.cancerdiagnosis'
        try:
            model_cls.objects.get(
                subject_visit=visit, results_to_record__in=[tb])
        except model_cls.DoesNotExist:
            return False
        return True

    def func_none_selection(self, visit=None, **kwargs):
        if_none = f'{self.app_label}.resultstorecord'.objects.get(name='none')
        model_cls = f'{self.app_label}.cancerdiagnosis'
        try:
            model_cls.objects.get(
                subject_visit=visit, results_to_record__in=[if_none])
        except model_cls.DoesNotExist:
            return False
        return True

    def func_hiv_result(self, visit=None, **kwargs):
        hiv_result = self.exists(
            reference_name=f'{self.app_label}.symptomsandtesting',
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name='hiv_result')
        hiv_test_result = self.exists(
            reference_name=f'{self.app_label}.symptomsandtesting',
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name='hiv_test_result')
        return hiv_result[0] == POS or hiv_test_result[0] == POS
