from unittest.mock import patch
from hestia_earth.schema import TermTermType

from hestia_earth.models.geospatialDatabase.utils import get_region_factor, get_area_size

class_path = 'hestia_earth.models.geospatialDatabase.utils'

AREA = 1000
COUNTRY = {
    '@id': 'GADM-ALB',
    'area': AREA
}


def test_get_region_factor():
    site = {'country': COUNTRY}
    assert get_region_factor('croppingIntensity', site, TermTermType.LANDUSEMANAGEMENT) == 0.9999775685587958


@patch(f"{class_path}.download_term", return_value={'area': AREA})
def test_get_area_size(*args):
    site = {'country': COUNTRY}
    assert get_area_size(site) == AREA

    site['boundary'] = {'type': 'Polygon'}
    site['boundaryArea'] = AREA
    assert get_area_size(site) == AREA
