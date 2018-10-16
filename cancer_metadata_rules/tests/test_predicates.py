from datetime import datetime

from arrow.arrow import Arrow
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_constants.constants import YES, NO, POS, NEG

from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from ..predicates import Predicates


@tag('1')
class TestPredicates(TestCase):

    reference_helper_cls = ReferenceTestHelper
    visit_model = 'cancer_subject.subjectvisit'
    reference_model = 'edc_reference.reference'
    app_label = 'cancer_subject'

    def setUp(self):
        self.subject_identifier = '111111111'
        self.reference_helper = self.reference_helper_cls(
            visit_model=self.visit_model,
            subject_identifier=self.subject_identifier)

        report_datetime = Arrow.fromdatetime(
            datetime(2017, 7, 7)).datetime
        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='1000')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint='1003')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=5),
            timepoint='1005')

    @property
    def subject_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')

    def test_oncology_plan_1(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan=YES,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_oncology_plan(self.subject_visits[0]))

    def test_oncology_plan_2(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan=NO,
            visit_code=self.subject_visits[0].visit_code)
        self.assertFalse(pc.func_oncology_plan(self.subject_visits[0]))

    def test_oncology_record_1(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received=YES,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_oncology_record(self.subject_visits[0]))

    def test_oncology_record_2(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received=NO,
            visit_code=self.subject_visits[0].visit_code)
        self.assertFalse(pc.func_oncology_record(self.subject_visits[0]))

    def test_oncology_1(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan=NO,
            visit_code=self.subject_visits[0].visit_code)
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received=NO,
            visit_code=self.subject_visits[0].visit_code)
        self.assertFalse(pc.func_oncology(self.subject_visits[0]))

    def test_oncology_2(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan=YES,
            visit_code=self.subject_visits[0].visit_code)
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received=YES,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_oncology(self.subject_visits[0]))

    def test_oncology_3(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan=NO,
            visit_code=self.subject_visits[0].visit_code)
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received=YES,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_oncology(self.subject_visits[0]))

    def test_oncology_4(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan=YES,
            visit_code=self.subject_visits[0].visit_code)
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received=NO,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_oncology(self.subject_visits[0]))

    def test_oncology_5(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentplan',
            radiation_plan='BLAH',
            visit_code=self.subject_visits[0].visit_code)
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.oncologytreatmentrecord',
            radiation_received='BLAH',
            visit_code=self.subject_visits[0].visit_code)
        self.assertFalse(pc.func_oncology(self.subject_visits[0]))

    def test_hiv_result_1(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.symptomsandtesting',
            hiv_result=POS,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_hiv_result(self.subject_visits[0]))

    def test_hiv_result_2(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.symptomsandtesting',
            hiv_test_result=POS,
            visit_code=self.subject_visits[0].visit_code)
        self.assertTrue(pc.func_hiv_result(self.subject_visits[0]))

    def test_hiv_result_3(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.symptomsandtesting',
            hiv_result=NEG,
            hiv_test_result=NEG,
            visit_code=self.subject_visits[0].visit_code)
        self.assertFalse(pc.func_hiv_result(self.subject_visits[0]))

#     @tag('1')
#     def test_haematology_1(self):
#         pc = Predicates()
#         haematology = ResultsToRecord.objects.create(name='haematology')
#
#         CancerDiagnosis.objects.create(results_to_record=haematology)
#         self.assertFalse(pc.func_haematology(self.subject_visits[0]))
