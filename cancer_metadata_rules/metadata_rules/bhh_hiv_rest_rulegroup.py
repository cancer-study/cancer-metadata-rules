from edc_constants.constants import POS
from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRule, register
from edc_metadata_rules import CrfRuleGroup
from edc_metadata_rules import P

app_label = 'cancer_subject'


@register()
class BHHHivTestRuleGroup(CrfRuleGroup):

    has_hiv_result = CrfRule(
        predicate=P('hiv_result', 'eq', POS),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.haartrecord'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.bhhhivtest'
