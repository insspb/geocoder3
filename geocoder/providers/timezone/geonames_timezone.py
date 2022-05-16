__all__ = ["GeonamesTimezone"]

from geocoder.location import Location
from geocoder.providers.addresses import GeonamesQuery, GeonamesResult


class GeonamesTimezoneResult(GeonamesResult):
    """Get timezone information for given lat,lng"""

    @property
    def sunrise(self):
        return self.raw_json.get("sunrise")

    @property
    def gmt_offset(self):
        return self.raw_json.get("gmtOffset")

    @property
    def raw_offset(self):
        return self.raw_json.get("rawOffset")

    @property
    def dst_offest(self):
        return self.raw_json.get("dstOffset")

    @property
    def sunset(self):
        return self.raw_json.get("sunset")

    @property
    def timezone_id(self):
        return self.raw_json.get("timezoneId")

    @property
    def time(self):
        return self.raw_json.get("time")


class GeonamesTimezone(GeonamesQuery):
    """Details:
    http://api.geonames.org/timezoneJSON?lat=47.01&lng=10.2
    """

    provider = "geonames"
    method = "timezone"

    _URL = "http://api.geonames.org/timezoneJSON"
    _RESULT_CLASS = GeonamesTimezoneResult

    def _build_params(self, location, provider_key, **kwargs):
        """Will be overridden according to the targetted web service"""
        location = Location(location)
        return {
            "lat": location.latitude,
            "lng": location.longitude,
            "username": provider_key,
        }

    def _adapt_results(self, json_response):
        # the returned JSON contains the object.
        # Need to wrap it into an array
        return [json_response]
