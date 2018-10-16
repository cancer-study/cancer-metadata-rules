from django.db import models
from edc_base.model_mixins import ListModelMixin, BaseUuidModel


class ResultsToRecord(ListModelMixin, BaseUuidModel):

    name = models.CharField(
        verbose_name='Name',
        max_length=250,
    )

    class Meta:
        app_label = 'cancer_metadata_rules'


class CancerDiagnosis(models.Model):
    results_to_record = models.ManyToManyField(
        ResultsToRecord,
        blank=True,)

    class Meta:
        app_label = "cancer_metadata_rules"
