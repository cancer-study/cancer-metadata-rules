from edc_constants.constants import NO, YES
from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRule, register
from edc_metadata_rules import CrfRuleGroup
from edc_metadata_rules import P

from ..predicates import func_oncology

app_label = 'cancer_subject'


@register()
class OncologyTreatmentCompletedRuleGroup(CrfRuleGroup):

    patient_had_chemo = CrfRule(
        predicate=P('patient_had_chemo', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.otrchemo'])

    patient_had_radiation = CrfRule(
        predicate=P('patient_had_radiation', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.radiationtreatment'])

    patient_had_surgery = CrfRule(
        predicate=P('patient_had_surgery', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.otrsurgical'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.oncologytreatmentcompleted'
