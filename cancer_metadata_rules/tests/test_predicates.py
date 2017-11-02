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

