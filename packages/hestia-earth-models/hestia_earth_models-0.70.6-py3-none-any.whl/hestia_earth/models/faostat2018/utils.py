from hestia_earth.schema import TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import safe_parse_float, flatten

from hestia_earth.models.log import logger, debugMissingLookup, logRequirements, logShouldRun, debugValues
from hestia_earth.models.utils.animalProduct import (
    FAO_LOOKUP_COLUMN, FAO_EQUIVALENT_LOOKUP_COLUMN, get_animalProduct_lookup_value
)
from hestia_earth.models.utils.product import convert_product_to_unit
from hestia_earth.models.utils.impact_assessment import get_country_id, impact_end_year
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.lookup import get_region_lookup_value
from . import MODEL

LOOKUP_PREFIX = f"{TermTermType.REGION.value}-{TermTermType.ANIMALPRODUCT.value}-{FAO_LOOKUP_COLUMN}"
FAOSTAT_AREA_LOOKUP = 'region-faostatArea.csv'


def get_liveAnimal_to_animalProduct_id(product_term_id: str, column: str, **log_args):
    lookup_name = 'liveAnimal.csv'
    lookup = download_lookup(lookup_name)
    value = get_table_value(lookup, 'termid', product_term_id, column_name(column))
    debugMissingLookup(lookup_name, 'termid', product_term_id, column, value, model=MODEL, **log_args)
    return value


def product_equivalent_value(product: dict, year: int, country: str):
    term_id = product.get('term', {}).get('@id')
    fao_product_id = get_animalProduct_lookup_value(MODEL, term_id, FAO_EQUIVALENT_LOOKUP_COLUMN) or term_id
    grouping = get_animalProduct_lookup_value(MODEL, fao_product_id, FAO_LOOKUP_COLUMN)

    if not grouping or not fao_product_id:
        return None

    quantity_values = get_region_lookup_value(f"{LOOKUP_PREFIX}-productionQuantity.csv", country, grouping)
    quantity = safe_parse_float(extract_grouped_data_closest_date(quantity_values, year))

    head_values = get_region_lookup_value(f"{LOOKUP_PREFIX}-head.csv", country, grouping)
    head = safe_parse_float(extract_grouped_data_closest_date(head_values, year))

    # quantity is in Tonnes
    value = quantity * 1000 / head if head > 0 else 0

    fao_product_term = download_hestia(fao_product_id)
    fao_product = {'term': fao_product_term, 'value': [value]}

    # use the FAO value to convert it to the correct unit
    dest_unit = product.get('term', {}).get('units')
    conv_value = convert_product_to_unit(fao_product, dest_unit)

    logger.debug('model=%s, country=%s, grouping=%s, year=%s, quantity=%s, head=%s, value=%s, conv_value=%s',
                 MODEL, country, f"'{grouping}'", year, quantity, head, value, conv_value)

    return conv_value


def _split_delta(table_value: str, start_year: int, end_year: int):
    start_value = extract_grouped_data_closest_date(table_value, start_year)
    end_value = extract_grouped_data_closest_date(table_value, end_year)
    return safe_parse_float(end_value) - safe_parse_float(start_value) if all([
        start_value is not None, end_value is not None
    ]) else None


def get_sum_of_columns(country: str, year: int, columns_list: list) -> float:
    return sum(
        [safe_parse_float(
            extract_grouped_data_closest_date(
                data=get_region_lookup_value(FAOSTAT_AREA_LOOKUP, country, col, model=MODEL),
                year=year
            )
        ) for col in columns_list]
    )


def get_single_delta(country: str, start_year: int, end_year: int, column: str):
    return _split_delta(
        get_region_lookup_value(FAOSTAT_AREA_LOOKUP, country, column, model=MODEL), start_year, end_year
    )


def get_land_ratio(
    country: str, start_year: int, end_year: int, first_column: str, second_column: str, total_column: str = None
):
    """
    total_column is optional. Assumes that, if missing, total is the sum of values from first and second.
    """
    first_delta = _split_delta(
        get_region_lookup_value(FAOSTAT_AREA_LOOKUP, country, first_column, model=MODEL), start_year, end_year
    )
    second_delta = _split_delta(
        get_region_lookup_value(FAOSTAT_AREA_LOOKUP, country, second_column, model=MODEL), start_year, end_year
    )
    total_delta = (
        get_sum_of_columns(
            country=country,
            year=end_year,
            columns_list=[first_column, second_column]
        ) - get_sum_of_columns(
            country=country,
            year=start_year,
            columns_list=[first_column, second_column]
        )
    ) if total_column is None else _split_delta(
        get_region_lookup_value(FAOSTAT_AREA_LOOKUP, country, total_column, model=MODEL), start_year, end_year
    )

    return (None, None, None) if any([
        total_delta is None,
        first_delta is None,
        second_delta is None
    ]) else (total_delta, first_delta, second_delta)


def get_cropland_ratio(country: str, start_year: int, end_year: int):
    return get_land_ratio(
        country=country,
        start_year=start_year,
        end_year=end_year,
        first_column='Permanent crops',
        second_column='Arable land',
        total_column='Cropland'
    )


def get_change_in_harvested_area_for_crop(country_id: str, crop_name: str, start_year: int, end_year: int = 0):
    lookup_name = 'region-crop-cropGroupingFaostatProduction-areaHarvested.csv'
    value = get_region_lookup_value(lookup_name, country_id, crop_name)
    return safe_parse_float(
        extract_grouped_data_closest_date(value, start_year)
    ) if end_year == 0 or end_year == start_year else _split_delta(value, start_year, end_year)


def should_run_landTransformationFromCropland(term_id: str, impact: dict):
    indicators = [
        i for i in impact.get('emissionsResourceUse', [])
        if all([
            i.get('term', {}).get('@id') == term_id,
            i.get('previousLandCover', {}).get('@id') == 'cropland',
            (i.get('value') or -1) > 0
        ])
    ]
    has_cropland = bool(indicators)

    should_run = all([has_cropland])
    logRequirements(impact, model=MODEL, term=term_id,
                    has_cropland_indicators=has_cropland)
    logShouldRun(impact, MODEL, term_id, should_run)

    return should_run, indicators


def run_landTransformationFromCropland(term_id: str, impact: dict, indicators: list, years: int):
    country_id = get_country_id(impact)
    end_year = impact_end_year(impact)
    total, permanent, temporary = get_cropland_ratio(country_id, end_year - years, end_year)

    debugValues(impact, model=MODEL, term_id=term_id,
                diff_temporary_area=temporary,
                diff_permanent_area=permanent,
                diff_total_area=total)

    return flatten([
        [
            _new_indicator(term_id, MODEL, indicator.get('landCover', {}).get('@id'), 'annualCropland') | {
                'value': indicator.get('value') * temporary / total
            },
            _new_indicator(term_id, MODEL, indicator.get('landCover', {}).get('@id'), 'permanentCropland') | {
                'value': indicator.get('value') * permanent / total
            }
        ]
        for indicator in indicators
    ]) if total is not None else []
