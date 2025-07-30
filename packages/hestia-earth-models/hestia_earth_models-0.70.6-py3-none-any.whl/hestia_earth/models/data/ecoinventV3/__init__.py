import os
from functools import lru_cache
from hestia_earth.utils.lookup import column_name, get_table_value, load_lookup, lookup_columns
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import logger

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_FILEPATH = os.getenv('ECOINVENT_V3_FILEPATH', f"{os.path.join(CURRENT_DIR, 'ecoinventV3_excerpt')}.csv")


@lru_cache()
def _get_file():
    if not os.path.exists(_FILEPATH):
        logger.warning('Ecoinvent file not found. Please make sure to set env variable "ECOINVENT_V3_FILEPATH".')
        return None

    return load_lookup(filepath=_FILEPATH, keep_in_memory=True)


def ecoinventV3_emissions(ecoinventName: str):
    lookup = _get_file()
    col_name = column_name('ecoinventName')

    def emission(column: str):
        id = get_table_value(lookup, col_name, ecoinventName, column_name(column))
        value = get_table_value(lookup, col_name, ecoinventName, column_name(column.replace('termid', 'value')))
        return (id, value) if id else None

    columns = [
        col for col in lookup_columns(lookup)
        if col.endswith(column_name('termid'))
    ]
    return non_empty_list(map(emission, columns))
