from django.db import models
from edc_base.model_mixins import ListModelMixin, BaseUuidModel
from edc_appointment.models.appointment import Appointment
from django.db.models.deletion import PROTECT
from edc_base.utils import get_utcnow


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class ResultsToRecord(ListModelMixin, BaseUuidModel):

    name = models.CharField(
        verbose_name='Name',
        max_length=250,
    )

    class Meta:
        app_label = 'cancer_metadata_rules'


class SubjectVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    def save(self, *args, **kwargs):
        self.visit_code = self.appointment.visit_code
        self.subject_identifier = self.appointment.subject_identifier
        super().save(*args, **kwargs)


class CancerDiagnosis(models.Model):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    results_to_record = models.ManyToManyField(
        ResultsToRecord,
        blank=True,
        null=True)

    class Meta:
        app_label = "cancer_metadata_rules"
