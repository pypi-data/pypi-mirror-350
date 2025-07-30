from functools import reduce
from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.tools import flatten, list_sum

from hestia_earth.models.log import debugValues, logShouldRun, logRequirements
from hestia_earth.models.data.ecoinventV3 import ecoinventV3_emissions
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.background_emissions import get_background_inputs, no_gap_filled_background_emissions
from hestia_earth.models.utils.blank_node import group_by_keys
from hestia_earth.models.utils.pesticideAI import get_pesticides_from_inputs
from hestia_earth.models.utils.fertiliser import get_fertilisers_from_inputs
from .utils import get_input_mappings

REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "value": "> 0",
            "none": {
                "fromCycle": "True",
                "producedInCycle": "True"
            }
        }],
        "optional": {
            "animals": [{
                "@type": "Animal",
                "inputs": [{
                    "@type": "Input",
                    "value": "> 0",
                    "none": {
                        "fromCycle": "True",
                        "producedInCycle": "True"
                    }
                }]
            }]
        }
    }
}
RETURNS = {
    "Emission": [{
        "term": "",
        "value": "",
        "methodTier": "background",
        "inputs": "",
        "operation": "",
        "animals": ""
    }]
}
LOOKUPS = {
    "electricity": "ecoinventMapping",
    "fuel": "ecoinventMapping",
    "inorganicFertiliser": "ecoinventMapping",
    "material": "ecoinventMapping",
    "pesticideAI": "ecoinventMapping",
    "soilAmendment": "ecoinventMapping",
    "transport": "ecoinventMapping",
    "veterinaryDrugs": "ecoinventMapping",
    "feedFoodAdditive": "ecoinventMapping"
}
MODEL = 'ecoinventV3'
MODEL_KEY = 'impactAssessment'  # keep to generate entry in "model-links.json"
TIER = EmissionMethodTier.BACKGROUND.value


def _emission(term_id: str, value: float, input: dict):
    emission = _new_emission(term_id, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['inputs'] = [input.get('term')]
    if input.get('operation'):
        emission['operation'] = input.get('operation')
    if input.get('animal'):
        emission['animals'] = [input.get('animal')]
    return emission


def _add_emission(cycle: dict, input: dict):
    input_term_id = input.get('term', {}).get('@id')
    operation_term_id = input.get('operation', {}).get('@id')
    animal_term_id = input.get('animal', {}).get('@id')

    def add(prev: dict, mapping: tuple):
        ecoinventName, coefficient = mapping
        emissions = ecoinventV3_emissions(ecoinventName)
        for emission_term_id, value in emissions:
            # log run on each emission so we know it did run
            debugValues(cycle, model=MODEL, term=emission_term_id,
                        value=value,
                        coefficient=coefficient,
                        input=input_term_id,
                        operation=operation_term_id,
                        animal=animal_term_id)
            prev[emission_term_id] = prev.get(emission_term_id, 0) + (value * coefficient)
        return prev
    return add


def _run_input(cycle: dict):
    no_gap_filled_background_emissions_func = no_gap_filled_background_emissions(cycle)

    def run(inputs: list):
        input = inputs[0]
        input_term_id = input.get('term', {}).get('@id')
        input_value = list_sum(flatten(input.get('value', []) for input in inputs))
        mappings = get_input_mappings(MODEL, cycle, input)
        has_mappings = len(mappings) > 0

        # skip input that has background emissions we have already gap-filled (model run before)
        has_no_gap_filled_background_emissions = no_gap_filled_background_emissions_func(input)

        logRequirements(cycle, model=MODEL, term=input_term_id,
                        has_ecoinvent_mappings=has_mappings,
                        ecoinvent_mappings=';'.join([v[0] for v in mappings]),
                        has_no_gap_filled_background_emissions=has_no_gap_filled_background_emissions,
                        input_value=input_value)

        should_run = all([has_mappings, has_no_gap_filled_background_emissions, input_value])
        logShouldRun(cycle, MODEL, input_term_id, should_run, methodTier=TIER)

        grouped_emissions = reduce(_add_emission(cycle, input), mappings, {}) if should_run else {}
        return [
            _emission(term_id, value * input_value, input)
            for term_id, value in grouped_emissions.items()
        ]
    return run


def run(_, cycle: dict):
    extra_inputs = get_pesticides_from_inputs(cycle) + get_fertilisers_from_inputs(cycle)
    inputs = get_background_inputs(cycle, extra_inputs=extra_inputs)
    grouped_inputs = reduce(group_by_keys(['term', 'operation', 'animal']), inputs, {})
    return flatten(map(_run_input(cycle), grouped_inputs.values()))
