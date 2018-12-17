from edc_constants.constants import DONT_KNOW, NO

from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRuleGroup, register
from edc_metadata_rules import CrfRule
from edc_metadata_rules import P, PF


app_label = 'cancer_subject'


@register()
class BaselineHIVHistoryRuleGroup(CrfRuleGroup):

    has_hiv_result = CrfRule(
        predicate=PF(
            'has_hiv_result',
            func=lambda has_smoked: True if has_smoked in [NO, DONT_KNOW] else False),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.bhhhivtest'])

    had_who_illnesses = CrfRule(
        predicate=P('had_who_illnesses', 'eq', NO),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.bhhwhoillness'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.baselinehivhistory'