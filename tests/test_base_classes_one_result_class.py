"""Tests for OneResult class

There are much more tests, that usually required. This done consciously as it is core
class of all future providers
"""
from typing import Optional, Type

import pytest

from geocoder.base import OneResult


@pytest.fixture()
def valid_result_class() -> Type[OneResult]:
    """Return Result class fixture type"""

    class ValidResultClass(OneResult):
        """Result class fixture"""

        _GEOCODER3_READY = True

        @property
        def lat(self) -> Optional[float]:
            """Latitude of the object"""
            return None

        @property
        def lng(self) -> Optional[float]:
            """Longitude of the object"""
            return None

        @property
        def address(self) -> Optional[str]:
            """Object simple string address."""
            return None

    return ValidResultClass


class TestCustomAndMagicMethods:
    def test__eq__match_two_objects_with_not_same_json_order(self, valid_result_class):
        results_a = valid_result_class({"prop1": "a", "prop2": "b"})
        results_b = valid_result_class({"prop2": "b", "prop1": "a"})

        assert results_b == results_a

    @pytest.mark.parametrize(
        "dict_a, dict_b",
        [
            ({"prop1": "b", "prop2": "a"}, {"prop1": "a", "prop2": "b"}),
            ({"prop1": "a", "prop2": "a"}, {"prop1": "a", "prop22": "a"}),
            ({"prop1": "a", "prop2": "a"}, {"prop1": "a", "prop2": "a", "prop3": "a"}),
        ],
        ids=[
            "Same keys, different values",
            "Same values, different keys",
            "Different sizes",
        ],
    )
    def test__eq__not_match_two_objects(self, valid_result_class, dict_a, dict_b):
        results_a = valid_result_class(dict_a)
        results_b = valid_result_class(dict_b)

        assert results_b != results_a


class TestInitSubclassMagicMethod:
    def test___init_subclass__raise_error__when_lat_property_not_implemented(self):
        with pytest.raises(NotImplementedError) as err:

            # noinspection PyAbstractClass
            class _(OneResult):
                """Test result class without lat property"""

                _GEOCODER3_READY = True

                @property
                def lng(self) -> Optional[float]:
                    """Longitude of the object"""
                    return None

                @property
                def address(self) -> Optional[str]:
                    """Object simple string address."""
                    return None

        assert str(err.value) == "All subclasses should implement 'lat' property"

    def test___init_subclass__raise_error__when_lng_property_not_implemented(self):
        with pytest.raises(NotImplementedError) as err:

            # noinspection PyAbstractClass
            class _(OneResult):
                """Test result class without lng property"""

                _GEOCODER3_READY = True

                @property
                def lat(self) -> Optional[float]:
                    """Latitude of the object"""
                    return None

                @property
                def address(self) -> Optional[str]:
                    """Object simple string address."""
                    return None

        assert str(err.value) == "All subclasses should implement 'lng' property"

    def test___init_subclass__raise_error__when_address_property_not_implemented(self):
        with pytest.raises(NotImplementedError) as err:

            # noinspection PyAbstractClass
            class _(OneResult):
                """Test result class without address property"""

                _GEOCODER3_READY = True

                @property
                def lat(self) -> Optional[float]:
                    """Latitude of the object"""
                    return None

                @property
                def lng(self) -> Optional[float]:
                    """Longitude of the object"""
                    return None

        assert str(err.value) == "All subclasses should implement 'address' property"
