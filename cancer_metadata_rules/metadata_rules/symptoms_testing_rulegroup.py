from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRule, register
from edc_metadata_rules import CrfRuleGroup

from ..predicates import Predicates

app_label = 'cancer_subject'
pc = Predicates()


@register()
class SymptomsTestingRuleGroup(CrfRuleGroup):

    hiv_test_result = CrfRule(
        predicate=pc.func_hiv_result,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.baselinehivhistory',
                       f'{app_label}.bhhhivtest',
                       f'{app_label}.bhhwhoillness',
                       f'{app_label}.haartrecord'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.symptomsandtesting'
