from arrow.arrow import Arrow
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag

from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from ..predicates import Predicates
from edc_constants.constants import YES


class TestPredicates(TestCase):

    reference_helper_cls = ReferenceTestHelper
    visit_model = 'ambition_subject.subjectvisit'
    reference_model = 'edc_reference.reference'
    app_label = 'ambition_subject'

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

    def test_cd4_requisition_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            cd4_date=(self.subject_visits[0].report_datetime - relativedelta(months=4)).date())
        self.assertTrue(pc.func_require_cd4(self.subject_visits[0]))

    def test_cd4_requisition_not_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            cd4_date=(self.subject_visits[0].report_datetime).date())
        self.assertFalse(pc.func_require_cd4(self.subject_visits[0]))

    def test_vl_requisition_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            viral_load_date=(self.subject_visits[0].report_datetime - relativedelta(months=4)).date())
        self.assertTrue(pc.func_require_vl(self.subject_visits[0]))

    def test_vl_requisition_not_required(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.patienthistory',
            visit_code=self.subject_visits[0].visit_code,
            viral_load_date=(self.subject_visits[0].report_datetime).date())
        self.assertFalse(pc.func_require_vl(self.subject_visits[0]))

    def test_ae_not_reqiuired_visit_1000(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[0].report_datetime,
            reference_name=f'{self.app_label}.bloodresult',
            visit_code=self.subject_visits[0].visit_code,
            abnormal_results_in_ae_range=YES)
        self.assertFalse(pc.func_require_ae(self.subject_visits[0]))

    def test_ae_reqiuired_visit_1003(self):
        pc = Predicates()
        self.reference_helper.create_for_model(
            report_datetime=self.subject_visits[1].report_datetime,
            reference_name=f'{self.app_label}.bloodresult',
            visit_code=self.subject_visits[1].visit_code,
            abnormal_results_in_ae_range=YES)
        self.assertTrue(pc.func_require_ae(self.subject_visits[1]))
