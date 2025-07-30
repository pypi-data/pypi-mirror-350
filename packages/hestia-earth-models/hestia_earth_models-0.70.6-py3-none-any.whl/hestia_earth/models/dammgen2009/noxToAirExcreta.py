from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.input import total_excreta
from hestia_earth.models.utils.excretaManagement import get_lookup_factor
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "practices": [
            {"@type": "Practice", "value": "", "term.termType": "excretaManagement"}
        ]
    }
}
LOOKUPS = {
    "excretaManagement": "EF_NO-N"
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}
TERM_ID = 'noxToAirExcreta'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _run(excretaKgN: float, NO_N_EF: float):
    value = (NO_N_EF or 0) * (excretaKgN or 0) * get_atomic_conversion(Units.KG_NOX, Units.TO_N)
    return [_emission(value)]


def _should_run(cycle: dict):
    excretaKgN = total_excreta(cycle.get('inputs', []))
    NO_N_EF = get_lookup_factor(cycle.get('practices', []), LOOKUPS['excretaManagement'])

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    excretaKgN=excretaKgN,
                    NO_N_EF=NO_N_EF)

    should_run = all([excretaKgN is not None, NO_N_EF is not None])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, excretaKgN, NO_N_EF


def run(cycle: dict):
    should_run, excretaKgN, NO_N_EF = _should_run(cycle)
    return _run(excretaKgN, NO_N_EF) if should_run else []
