from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, CycleFunctionalUnit
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import safe_parse_float, non_empty_list

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.blank_node import get_lookup_value
from hestia_earth.models.utils.emission import _new_emission
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "cycleDuration": "",
        "functionalUnit": "relative",
        "site": {
            "@type": "Site",
            "area": "",
            "measurements": [{
                "@type": "Measurement",
                "term.@id": [
                    "salineWater",
                    "brackishWater",
                    "freshWater"
                ]
            }]
        }
    }
}
LOOKUPS = {
    "measurement": "IPCC_2019_CH4_aquaculture_EF"
}
RETURNS = {
    "Emission": [{
        "value": "",
        "min": "",
        "max": "",
        "methodTier": "tier 1",
        "statsDefinition": "modelled"
    }]
}
TERM_ID = 'ch4ToAirAquacultureSystems'
TIER = EmissionMethodTier.TIER_1.value
_WATER_TERM_IDS = [
    'salineWater',
    'brackishWater',
    'freshWater'
]


def _emission(value: float, min: float, max: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['min'] = [min]
    emission['max'] = [max]
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    emission['methodTier'] = TIER
    return emission


def _find_measurement(site: dict):
    measurements = non_empty_list([
        find_term_match(site.get('measurements', []), term_id, None) for term_id in _WATER_TERM_IDS
    ])
    return measurements[0] if measurements else None


def _run(cycle: dict):
    cycle_duration = cycle.get('cycleDuration')
    site = cycle.get('site', {})
    site_area = site.get('area')
    water_term = _find_measurement(site).get('term', {})
    factor_value = safe_parse_float(get_lookup_value(water_term, LOOKUPS.get('measurement')))
    factor_min = safe_parse_float(get_lookup_value(water_term, f"{LOOKUPS.get('measurement')}-min"))
    factor_max = safe_parse_float(get_lookup_value(water_term, f"{LOOKUPS.get('measurement')}-max"))
    ratio = site_area * cycle_duration / 365
    return [_emission(ratio * factor_value, ratio * factor_min, ratio * factor_max)]


def _should_run(cycle: dict):
    cycle_duration = cycle.get('cycleDuration')
    is_relative = cycle.get('functionalUnit') == CycleFunctionalUnit.RELATIVE.value
    site = cycle.get('site', {})
    site_area = site.get('area')
    has_water_type = _find_measurement(site) is not None

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    cycle_duration=cycle_duration,
                    is_relative=is_relative,
                    site_area=site_area,
                    has_water_type=has_water_type)

    should_run = all([cycle_duration, is_relative, site_area, has_water_type])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else []
