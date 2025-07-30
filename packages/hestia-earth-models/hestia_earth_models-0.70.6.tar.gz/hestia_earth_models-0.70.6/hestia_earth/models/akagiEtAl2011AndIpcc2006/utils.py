from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import flatten

from hestia_earth.models.utils.completeness import _is_term_type_complete


def _get_crop_residue_burnt_value(cycle: dict):
    products = cycle.get('products', [])
    value = flatten([
        find_term_match(products, 'aboveGroundCropResidueBurnt').get('value', []),
        find_term_match(products, 'discardedCropBurnt').get('value', [])
    ])
    data_complete = _is_term_type_complete(cycle, TermTermType.CROPRESIDUE)
    return [0] if len(value) == 0 and data_complete else value
