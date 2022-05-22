__all__ = [
    "W3WResult",
    "W3WQuery",
    "W3WReverseResult",
    "W3WReverse",
]

import logging

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import w3w_key


class W3WResult(OneResult):
    @property
    def lat(self):
        position = self.object_raw_json.get("geometry")
        if position:
            return position["lat"]

    @property
    def lng(self):
        position = self.object_raw_json.get("geometry")
        if position:
            return position["lng"]

    @property
    def language(self):
        return self.object_raw_json.get("language")

    @property
    def words(self):
        return self.object_raw_json.get("words")


class W3WQuery(MultipleResultsQuery):
    """
    What3Words

    What3Words is a global grid of 57 trillion 3mx3m squares.
    Each square has a 3 word address that can be communicated quickly,
    easily and with no ambiguity.

    Addressing the world

    Everyone and everywhere now has an address

    :param location: Your search location you want geocoded.
    :param key: W3W API key.
    :param method: Chose a method (geocode, method)

    References

    API Reference: https://docs.what3words.com/api/v2/
    Get W3W key: https://map.what3words.com/register?dev=true
    """

    _PROVIDER = "w3w"
    _METHOD = "geocode"
    _URL = "https://api.what3words.com/v2/forward"
    _RESULT_CLASS = W3WResult
    _KEY = w3w_key

    def _build_params(self, location, provider_key, **kwargs):
        return {
            "addr": location,
            "key": provider_key,
        }

    def _adapt_results(self, json_response):
        return [json_response]


class W3WReverseResult(W3WResult):
    @property
    def ok(self):
        return bool(self.words)


class W3WReverse(W3WQuery):
    """
    what3words

    what3words is a global grid of 57 trillion 3mx3m squares.
    Each square has a 3 word address that can be communicated quickly,
    easily and with no ambiguity.

    Addressing the world

    Everyone and everywhere now has an address

    :param location: Your search location you want geocoded.
    :param key: W3W API key.
    :param method: Chose a method (geocode, method)

    API Reference: http://developer.what3words.com/
    Get W3W key: http://developer.what3words.com/api-register/
    """

    _PROVIDER = "w3w"
    _METHOD = "reverse"
    _URL = "https://api.what3words.com/v2/reverse"
    _RESULT_CLASS = W3WReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        return {
            "coords": location,
            "key": provider_key,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = W3WQuery("embedded.fizzled.trial")
    g.debug()
