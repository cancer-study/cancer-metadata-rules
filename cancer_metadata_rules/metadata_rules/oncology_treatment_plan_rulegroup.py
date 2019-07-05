from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRule, register
from edc_metadata_rules import CrfRuleGroup

from ..predicates import Predicates

app_label = 'cancer_subject'
pc = Predicates()


@register()
class OncologyTreatmentPlanRuleGroup(CrfRuleGroup):

    radiation_plan = CrfRule(
        predicate=pc.func_oncology,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.radiationtreatment'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.oncologytreatmentplan'
