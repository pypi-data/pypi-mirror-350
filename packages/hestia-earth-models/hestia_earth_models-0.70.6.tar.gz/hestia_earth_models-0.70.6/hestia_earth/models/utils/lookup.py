import functools
from typing import Optional, List
from hestia_earth.utils.lookup import (
    download_lookup,
    get_table_value,
    column_name,
    extract_grouped_data,
    _get_single_table_value,
    lookup_term_ids
)
from hestia_earth.utils.tools import list_sum, safe_parse_float

from ..log import debugValues, log_as_table, debugMissingLookup


def _node_value(node):
    value = node.get('value')
    return list_sum(value, default=None) if isinstance(value, list) else value


def _factor_value(model: str, term_id: str, lookup_name: str, lookup_col: str, grouped_key: Optional[str] = None):
    def get_value(data: dict):
        node_term_id = data.get('term', {}).get('@id')
        grouped_data_key = grouped_key or data.get('methodModel', {}).get('@id')
        value = _node_value(data)
        coefficient = get_region_lookup_value(lookup_name, node_term_id, lookup_col, model=model, term=term_id)
        # value is either a number or matching between a model and a value (restrict value to specific model only)
        coefficient = safe_parse_float(
            extract_grouped_data(coefficient, grouped_data_key),
            default=None
        ) if ':' in str(coefficient) else safe_parse_float(coefficient, None)
        if value is not None and coefficient is not None:
            if model:
                debugValues(data, model=model, term=term_id,
                            node=node_term_id,
                            operation=data.get('operation', {}).get('@id'),
                            value=value,
                            coefficient=coefficient)
        return {'id': node_term_id, 'value': value, 'coefficient': coefficient}
    return get_value


def _term_factor_value(model: str, term_id: str, lookup_name: str, lookup_term_id: str, group_key: str = None):
    def get_value(data: dict):
        node_term_id = data.get('term', {}).get('@id')
        value = _node_value(data)
        coefficient = get_region_lookup_value(lookup_name, lookup_term_id, node_term_id, model=model, term=term_id)
        coefficient = safe_parse_float(
            extract_grouped_data(coefficient, group_key) if group_key else coefficient,
            default=None
        )
        if value is not None and coefficient is not None:
            debugValues(data, model=model, term=term_id,
                        node=node_term_id,
                        value=value,
                        coefficient=coefficient)
        return {'id': node_term_id, 'value': value, 'coefficient': coefficient}
    return get_value


def _aware_factor_value(model: str, term_id: str, lookup_name: str, aware_id: str, group_key: str = None):
    lookup = download_lookup(lookup_name, False)  # avoid saving in memory as there could be many different files used
    lookup_col = column_name('awareWaterBasinId')

    def get_value(data: dict):
        node_term_id = data.get('term', {}).get('@id')
        value = _node_value(data)

        try:
            coefficient = _get_single_table_value(lookup, lookup_col, int(aware_id), column_name(node_term_id))
            coefficient = safe_parse_float(
                extract_grouped_data(coefficient, group_key),
                default=None
            ) if group_key else coefficient
            if value is not None and coefficient is not None:
                debugValues(data, model=model, term=term_id,
                            node=node_term_id,
                            value=value,
                            coefficient=coefficient)
        except ValueError:  # factor does not exist
            coefficient = None

        return {'id': node_term_id, 'value': value, 'coefficient': coefficient}
    return get_value


def all_factor_value(
    model: str,
    term_id: str,
    node: dict,
    lookup_name: str,
    lookup_col: str,
    blank_nodes: List[dict],
    grouped_key: Optional[str] = None,
    default_no_values=0,
    factor_value_func=_factor_value
):
    values = list(map(factor_value_func(model, term_id, lookup_name, lookup_col, grouped_key), blank_nodes))

    has_values = len(values) > 0
    missing_values = set([v.get('id') for v in values if v.get('value') and v.get('coefficient') is None])
    all_with_factors = not missing_values

    for missing_value in missing_values:
        debugMissingLookup(lookup_name, 'termid', missing_value, lookup_col, None, model=model, term=term_id)

    debugValues(node, model=model, term=term_id,
                all_with_factors=all_with_factors,
                missing_lookup_factor=';'.join(missing_values),
                has_values=has_values,
                values_used=log_as_table(values))

    values = [float((v.get('value') or 0) * (v.get('coefficient') or 0)) for v in values]

    # fail if some factors are missing
    return None if not all_with_factors else (list_sum(values) if has_values else default_no_values)


def _country_in_lookup(country_id: str):
    def in_lookup(lookup_name: str):
        return (
            download_lookup(lookup_name.replace('region', country_id)) is not None or
            country_id in lookup_term_ids(download_lookup(lookup_name))
        )
    return in_lookup


def fallback_country(country_id: str, lookups: List[str]) -> str:
    """
    Given a country `@id`, and lookup tables, checks if a location can be used in lookup file
    else fallback to the default "region-world".
    """
    is_in_lookup = lambda v: all(map(_country_in_lookup(v), lookups))  # noqa: E731
    fallback_id = 'region-world'
    return country_id if country_id and is_in_lookup(country_id) else fallback_id if is_in_lookup(fallback_id) else None


@functools.cache
def get_region_lookup_value(lookup_name: str, term_id: str, column: str, **log_args):
    # for performance, try to load the region specific lookup if exists
    lookup = (
        download_lookup(lookup_name.replace('region-', f"{term_id}-"))
        if lookup_name and lookup_name.startswith('region-') else None
    ) or download_lookup(lookup_name)
    value = get_table_value(lookup, 'termid', term_id, column_name(column))
    debugMissingLookup(lookup_name, 'termid', term_id, column, value, **log_args)
    return value
