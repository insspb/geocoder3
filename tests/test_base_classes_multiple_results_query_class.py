"""Tests for MultipleResultsQuery class

There are much more tests, that usually required. This done consciously as it is core
class of all future providers
"""
import logging
from typing import Optional, Type

import pytest

from geocoder.base import MultipleResultsQuery, OneResult


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


@pytest.fixture()
def valid_query_class(valid_result_class) -> Type[MultipleResultsQuery]:
    """Return Query class fixture type"""

    class ValidQueryClass(MultipleResultsQuery):
        """Query class fixture"""

        _URL = "http://localhost"
        _RESULT_CLASS = valid_result_class
        _METHOD = "geocode"
        _KEY = None
        _KEY_MANDATORY = False
        _PROVIDER = "test_provider"
        _GEOCODER3_READY = True

    return ValidQueryClass


class TestIsValidUrlPrivateMethod:
    @pytest.mark.parametrize(
        "valid_url",
        [
            "http://localhost",
            "http://localhost/",
            "https://localhost",
            "https://localhost/",
            "https://nominatim.openstreetmap.org/search",
            "https://nominatim.openstreetmap.org/search/",
            "http://nominatim.openstreetmap.org/search",
            "http://nominatim.openstreetmap.org/search/",
        ],
    )
    def test__is_valid_url__returns_true__if_url_is_correct(self, valid_url):
        result = MultipleResultsQuery._is_valid_url(valid_url)

        assert result is True

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "httxp://localhost",
            "httxp://localhost/",
            "localhost",
            "localhost/",
            None,
            1,
        ],
    )
    def test__is_valid_url__returns_false__if_url_is_incorrect(self, invalid_url):
        result = MultipleResultsQuery._is_valid_url(invalid_url)

        assert result is False

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "httxp://localhost",
            "httxp://localhost/",
            "localhost",
            "localhost/",
            1,
        ],
    )
    def test__is_valid_url__trigger__init__method_to_raise_error__when_url_is_incorrect(
        self,
        valid_query_class,
        invalid_url,
    ):
        with pytest.raises(ValueError) as err:
            _ = valid_query_class("Fake Location", url=invalid_url)

        assert str(err.value) == f"url not valid. Got {invalid_url}"


class TestInitSubclassMagicMethod:
    @pytest.mark.parametrize(
        "invalid_url",
        [
            "httxp://localhost",
            "httxp://localhost/",
            "localhost",
            "localhost/",
            None,
            1,
        ],
    )
    def test___init_subclass__raise_error__when_url_is_malformed(
        self, valid_query_class, invalid_url
    ):
        with pytest.raises(ValueError) as err:

            class _(valid_query_class):
                _URL = invalid_url

        assert "Subclass must define a valid URL." in str(err.value)

    def test___init_subclass__raise_error__when_subclass_is_none(
        self, valid_query_class
    ):
        with pytest.raises(ValueError) as err:

            class _(valid_query_class):
                _RESULT_CLASS = None

        assert (
            str(err.value) == "Subclass must define _RESULT_CLASS from 'OneResult'. "
            "Got None"
        )

    def test___init_subclass__raise_error__when_subclass_is_not_from_one_result_class(
        self,
        valid_query_class,
    ):
        with pytest.raises(ValueError) as err:

            class ResultForTest:
                """Class not nested from expected class"""

                pass

            class _(valid_query_class):
                _RESULT_CLASS = ResultForTest

        assert "Subclass must define _RESULT_CLASS from 'OneResult'." in str(err.value)

    @pytest.mark.parametrize("invalid_method", [None, "unsupported"])
    def test___init_subclass__raise_error__when_method_is_not_set_or_incorrect(
        self, valid_query_class, invalid_method
    ):
        with pytest.raises(ValueError) as err:

            class _(valid_query_class):
                _METHOD = invalid_method

        assert (
            "Subclass must define correct _METHOD attribute, not equal to None. "
            in str(err.value)
        )


class TestHasDataProperty:
    def test__has_data__raises_error__when_external_call_not_made(
        self, valid_query_class
    ):
        test_object = valid_query_class("Fake Location")
        with pytest.raises(RuntimeError) as err:
            _ = test_object.has_data

        assert str(err.value) == (
            "Cannot detect data presence. External request was not made. "
            "Use instance __call__() method to retrieve data."
        )


class TestStatusProperty:
    def test__status__display_correct_info__when_external_call_not_made(
        self, valid_query_class
    ):
        test_object = valid_query_class("Fake Location")
        assert test_object.status == "External request was not made"


class TestDebugFunction:
    def test__debug__when_query_not_made__return_only_status(
        self, caplog, valid_query_class
    ):
        caplog.set_level(logging.DEBUG)
        test_object = valid_query_class("Fake Location")
        _ = test_object.debug()
        assert "[External request was not made]" in caplog.text
        assert "Test_Provider - Geocode [empty]" in caplog.text
        assert "results: 0" in caplog.text
        assert "code: None" in caplog.text
        assert "url:  http://localhost" in caplog.text
        assert "External request was not made" in caplog.text


class TestApiKey:
    @pytest.mark.parametrize("wrong_key", ["", None], ids=["Empty", "None"])
    def test__get_api_key__raise_error__when_api_key_required_but_not_provided(
        self, valid_query_class, wrong_key
    ):
        class TestClass(valid_query_class):
            """Test class with modified _KEY_MANDATORY"""

            _KEY_MANDATORY = True

        with pytest.raises(ValueError) as err:
            _ = TestClass("Fake Location", key=wrong_key)

        assert str(err.value) == "Provide API Key"

    def test__get_api_key_and__init__correctly_set_key__when_api_key_and_provided(
        self, valid_query_class
    ):
        correct_key = "Any string"

        class TestClass(valid_query_class):
            """Test class with modified _KEY_MANDATORY and _KEY"""

            _KEY_MANDATORY = True
            _KEY = "I will be replaced"

        obj = TestClass("Fake Location", key=correct_key)
        assert obj._KEY == correct_key


class TestCollectionCustomAndMagicMethods:
    def test__add__method__adds_result_to_collection__even_when_not_yet_called(
        self, valid_query_class, valid_result_class
    ):
        collection = valid_query_class("Some location")
        fake_result = valid_result_class({})

        assert len(collection) == 0

        collection.add(fake_result)

        assert len(collection) == 1
        assert collection[0] == fake_result
