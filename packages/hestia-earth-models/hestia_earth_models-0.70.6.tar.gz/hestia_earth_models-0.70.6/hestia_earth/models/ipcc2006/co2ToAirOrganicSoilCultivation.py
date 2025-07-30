from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from hestia_earth.models.utils.ecoClimateZone import get_ecoClimateZone_lookup_value
from hestia_earth.models.utils.cycle import land_occupation_per_ha
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "or": [
            {
                "cycleDuration": "",
                "practices": [{"@type": "Practice", "value": "", "term.@id": "longFallowRatio"}]
            },
            {
                "@doc": "for plantations, additional properties are required",
                "practices": [
                    {"@type": "Practice", "value": "", "term.@id": "nurseryDensity"},
                    {"@type": "Practice", "value": "", "term.@id": "nurseryDuration"},
                    {"@type": "Practice", "value": "", "term.@id": "plantationProductiveLifespan"},
                    {"@type": "Practice", "value": "", "term.@id": "plantationDensity"},
                    {"@type": "Practice", "value": "", "term.@id": "plantationLifespan"},
                    {"@type": "Practice", "value": "", "term.@id": "rotationDuration"}
                ]
            }
        ],
        "site": {
            "@type": "Site",
            "measurements": [
                {"@type": "Measurement", "value": "", "term.@id": "histosol"},
                {"@type": "Measurement", "value": "", "term.@id": "ecoClimateZone"}
            ]
        },
        "optional": {
            "cycleDuration": ""
        }
    }
}
LOOKUPS = {
    "crop": "isPlantation",
    "ecoClimateZone": "IPCC_2006_ORGANIC_SOILS_TONNES_CO2-C_HECTARE"
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}
TERM_ID = 'co2ToAirOrganicSoilCultivation'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _run(histosol: float, organic_soil_factor: float, land_occupation: float):
    value = land_occupation * histosol / 100 * organic_soil_factor
    return [_emission(value)]


def _get_CO2_factor(eco_climate_zone: str, site_type: str):
    return get_ecoClimateZone_lookup_value(
        eco_climate_zone, LOOKUPS['ecoClimateZone'], site_type
    ) * 1000 * get_atomic_conversion(Units.KG_CO2, Units.TO_C)


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    site_type = site.get('siteType', None)
    measurements = site.get('measurements', [])

    def _get_measurement_content(term_id: str):
        return most_relevant_measurement_value(measurements, term_id, end_date)

    histosol = _get_measurement_content('histosol')
    eco_climate_zone = _get_measurement_content('ecoClimateZone')
    organic_soil_factor = _get_CO2_factor(eco_climate_zone, site_type) if eco_climate_zone else 0
    land_occupation = land_occupation_per_ha(MODEL, TERM_ID, cycle)

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    organic_soil_factor=organic_soil_factor,
                    land_occupation=land_occupation,
                    histosol=histosol)

    should_run = all([organic_soil_factor, land_occupation, histosol is not None])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, histosol, organic_soil_factor, land_occupation


def run(cycle: dict):
    should_run, histosol, organic_soil_factor, land_occupation = _should_run(cycle)
    return _run(histosol, organic_soil_factor, land_occupation) if should_run else []
