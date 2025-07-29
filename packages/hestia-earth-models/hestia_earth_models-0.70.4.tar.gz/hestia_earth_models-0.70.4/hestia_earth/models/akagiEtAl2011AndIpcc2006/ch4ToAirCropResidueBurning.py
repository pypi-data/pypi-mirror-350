from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.emission import _new_emission
from .utils import _get_crop_residue_burnt_value
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "or": {
            "products": [{
                "@type": "Product",
                "term.@id": ["aboveGroundCropResidueBurnt", "discardedCropBurnt"],
                "value": ""
            }],
            "completeness.cropResidue": "True"
        }
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}
TERM_ID = 'ch4ToAirCropResidueBurning'
TIER = EmissionMethodTier.TIER_1.value
DRY_MATTER_FACTOR_TO_CH4 = 5.82/1000


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _run(product_value: list):
    value = sum(product_value)
    return [_emission(value * DRY_MATTER_FACTOR_TO_CH4)]


def _should_run(cycle: dict):
    crop_residue_burnt_value = _get_crop_residue_burnt_value(cycle)
    has_crop_residue_burnt = len(crop_residue_burnt_value) > 0

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    has_crop_residue_burnt=has_crop_residue_burnt)

    should_run = all([has_crop_residue_burnt])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, crop_residue_burnt_value


def run(cycle: dict):
    should_run, crop_residue_burnt_value = _should_run(cycle)
    return _run(crop_residue_burnt_value) if should_run else []
