import pytest

import geocoder
from geocoder.distance import haversine


@pytest.mark.parametrize(
    "units, expected",
    [
        ("miles", 215.81976294960634),
        ("mile", 215.81976294960634),
        ("mi", 215.81976294960634),
        ("ml", 215.81976294960634),
        ("kilometers", 347.32834803942626),
        ("kilometres", 347.32834803942626),
        ("kilometer", 347.32834803942626),
        ("kilometre", 347.32834803942626),
        ("km", 347.32834803942626),
        ("meters", 347328.34803942626),
        ("metres", 347328.34803942626),
        ("meter", 347328.34803942626),
        ("metre", 347328.34803942626),
        ("m", 347328.34803942626),
        ("feet", 1139528.3483739216),
        ("f", 1139528.3483739216),
        ("ft", 1139528.3483739216),
    ],
)
class TestDistanceModuleCorrectResults:
    """
    Tests data based on article:
    https://www.igismap.com/haversine-formula-calculate-geographic-distance-earth/
    """

    NEBRASKA = geocoder.Location([41.507483, -99.436554])
    KANSAS = geocoder.Location([38.504048, -98.315949])

    def test__haversine_function__return_expected_results(self, units, expected):
        result = haversine(self.NEBRASKA, self.KANSAS, units=units)
        assert result == expected

    def test__get_distance_function__return_expected_results(self, units, expected):
        result = geocoder.Distance(self.NEBRASKA, self.KANSAS, units=units)
        assert result == expected
