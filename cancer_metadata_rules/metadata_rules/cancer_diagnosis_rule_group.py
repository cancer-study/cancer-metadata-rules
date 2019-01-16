from edc_metadata.constants import NOT_REQUIRED, REQUIRED

from edc_metadata_rules import CrfRule, register
from edc_metadata_rules import CrfRuleGroup


from ..predicates import Predicates

app_label = 'cancer_subject'
pc = Predicates()


@register()
class CancerDiagnosisRuleGroup(CrfRuleGroup):

    results_to_record_haem = CrfRule(
        predicate=pc.func_haematology,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.labresulthaematology'])

    results_to_record_chem = CrfRule(
        predicate=pc.func_chemistry,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.labresultchemistry'])

    results_to_record_tb = CrfRule(
        predicate=pc.func_tubercolosis,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.labresulttb'])

    results_to_record_none = CrfRule(
        predicate=pc.func_none_selection,
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.labresulthaematology',
                       f'{app_label}.labresultchemistry',
                       f'{app_label}.labresulttb'])

    class Meta:
        app_label = 'cancer_subject'
        source_model = f'{app_label}.cancerdiagnosis'
