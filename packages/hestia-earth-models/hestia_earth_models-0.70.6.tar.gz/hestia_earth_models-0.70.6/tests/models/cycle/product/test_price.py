import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.product.price import (
    MODEL, MODEL_KEY, run, _should_run_product_by_share_0
)

class_path = f"hestia_earth.models.{MODEL}.product.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/{MODEL}/product/{MODEL_KEY}"


def test_should_run_product_by_share_0():
    product = {'term': {'@id': 'citrusFruit', 'termType': 'crop'}}
    assert not _should_run_product_by_share_0({}, product)

    product = {'term': {'@id': 'nitrogenUptakeEdiblePart', 'termType': 'crop'}}
    assert _should_run_product_by_share_0({}, product) is True


def test_run():
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


def test_run_excreta():
    with open(f"{fixtures_folder}/excreta/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/excreta/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
