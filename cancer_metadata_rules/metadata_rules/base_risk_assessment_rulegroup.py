from edc_constants.constants import DECLINED, NO
from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRuleGroup
from edc_metadata_rules import CrfRule
from edc_metadata_rules import PF

app_label = 'cancer_subject'


class BaseRiskAssessmentRuleGroup(CrfRuleGroup):

    has_smoked = CrfRule(
        predicate=PF(
            'has_smoked',
            func=lambda has_smoked: True if has_smoked in [NO, DECLINED] else False),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.baseriskassessmentsmoking'])

    has_worked_mine = CrfRule(
        predicate=PF(
            'has_worked_mine',
            func=lambda has_worked_mine: True if has_worked_mine in [NO, DECLINED] else False),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.baseriskassessmentsmoking'])

    has_worked_mine = CrfRule(
        predicate=PF(
            'has_alcohol',
            func=lambda has_alcohol: True if has_alcohol in [NO, DECLINED] else False),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.baseriskassessmentsmoking'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.baseriskassessment'
