from edc_constants.constants import MALE
from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRuleGroup, register
from edc_metadata_rules import CrfRule
from edc_metadata_rules import PF

app_label = 'cancer_subject'


@register()
class GenderRuleGroup(CrfRuleGroup):

    gender = CrfRule(
        predicate=PF(
            'gender',
            func=lambda gender: True if gender in [MALE] else False),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.baseriskassessmentfemale'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.baseriskassessment'
