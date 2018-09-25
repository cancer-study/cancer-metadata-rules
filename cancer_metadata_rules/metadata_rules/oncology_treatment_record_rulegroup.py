from edc_constants.constants import NO, YES
from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRule, register
from edc_metadata_rules import CrfRuleGroup
from edc_metadata_rules import P

from ..predicates import func_oncology

app_label = 'cancer_subject'


@register()
class OncologyTreatmentRecordRuleGroup(CrfRuleGroup):

    chemo_received = CrfRule(
        predicate=P('chemo_received', 'eq', NO),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.otrchemo'])

    radiation_received = CrfRule(
        predicate=func_oncology,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.radiationtreatment'])

    surgical_therapy = CrfRule(
        predicate=P('surgical_therapy', 'eq', NO),
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.otrsurgical'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.oncologytreatmentrecord'
