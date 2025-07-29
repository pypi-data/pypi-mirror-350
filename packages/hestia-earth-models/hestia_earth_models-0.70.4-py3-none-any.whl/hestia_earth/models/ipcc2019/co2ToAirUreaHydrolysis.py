from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.tools import list_sum, safe_parse_float, non_empty_list
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.completeness import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.term import get_urea_terms
from hestia_earth.models.utils.inorganicFertiliser import get_country_breakdown, get_term_lookup
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.fertiliser": "",
        "inputs": [{"@type": "Input", "value": "", "term.termType": "inorganicFertiliser"}]
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}
LOOKUPS = {
    "inorganicFertiliser": ["Urea_UAS_Amm_Bicarb", "UAN_Solu", "CO2_urea_emissions_factor"]
}
TERM_ID = 'co2ToAirUreaHydrolysis'
TIER = EmissionMethodTier.TIER_1.value
UNSPECIFIED_TERM_ID = 'inorganicNitrogenFertiliserUnspecifiedKgN'


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _urea_input_value(cycle: dict):
    def exec(data: dict):
        term_id = data.get('id')
        values = data.get('values')
        coeff = safe_parse_float(get_term_lookup(term_id, LOOKUPS['inorganicFertiliser'][2]), 1)
        debugValues(cycle, model=MODEL, term=TERM_ID,
                    product=term_id,
                    coefficient=coeff)
        return list_sum(values) * coeff
    return exec


def _run(cycle: dict, urea_values: list):
    value = list_sum(list(map(_urea_input_value(cycle), urea_values)))
    return [_emission(value)]


def _get_urea_values(cycle: dict, inputs: list, term_id: str):
    inputs = list(filter(lambda i: i.get('term', {}).get('@id') == term_id, inputs))
    values = [list_sum(i.get('value'), 0) for i in inputs if len(i.get('value', [])) > 0]
    return [0] if len(inputs) == 0 and _is_term_type_complete(cycle, 'fertiliser') else values


def _should_run(cycle: dict):
    inputs = cycle.get('inputs', [])
    term_ids = get_urea_terms()

    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    urea_share = get_country_breakdown(MODEL, TERM_ID, country_id, LOOKUPS['inorganicFertiliser'][0])
    uan_share = get_country_breakdown(MODEL, TERM_ID, country_id, LOOKUPS['inorganicFertiliser'][1])
    urea_unspecified_as_n = list_sum(find_term_match(inputs, UNSPECIFIED_TERM_ID).get('value', []))

    urea_values = [
        {
            'id': id,
            'values': _get_urea_values(cycle, inputs, id)
        } for id in term_ids
    ] + non_empty_list([
        {
            'id': 'ureaKgN',
            'values': [urea_unspecified_as_n * urea_share]
        } if urea_share is not None else None,
        {
            'id': 'ureaAmmoniumNitrateKgN',
            'values': [urea_unspecified_as_n * uan_share]
        } if urea_share is not None else None
    ] if urea_unspecified_as_n > 0 else [])
    has_urea_value = any([len(data.get('values')) > 0 for data in urea_values])

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    has_urea_value=has_urea_value,
                    urea_unspecified_as_n=urea_unspecified_as_n,
                    urea_share=urea_share,
                    uan_share=uan_share)

    should_run = all([has_urea_value])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, urea_values


def run(cycle: dict):
    should_run, urea_values = _should_run(cycle)
    return _run(cycle, urea_values) if should_run else []
