__all__ = ["ArcgisQuery"]

import json
import logging

from geocoder.base import MultipleResultsQuery, OneResult


class ArcgisResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._feature = json_content.get("feature", {})

        # proceed with super.__init__
        super(ArcgisResult, self).__init__(json_content)

    @property
    def address(self):
        return self.raw_json.get("name", "")

    @property
    def lat(self):
        return self._feature.get("geometry", {}).get("y")

    @property
    def lng(self):
        return self._feature.get("geometry", {}).get("x")

    @property
    def score(self):
        return self._feature.get("attributes", {}).get("Score", "")

    @property
    def quality(self):
        return self._feature.get("attributes", {}).get("Addr_Type", "")

    @property
    def bbox(self):
        _extent = self.raw_json.get("extent")
        if _extent:
            south = _extent.get("ymin")
            west = _extent.get("xmin")
            north = _extent.get("ymax")
            east = _extent.get("xmax")
            return self._get_bbox(south, west, north, east)


class ArcgisQuery(MultipleResultsQuery):
    """
    ArcGIS REST API

    The World Geocoding Service finds addresses and places in all supported countries
    from a single endpoint. The service can find point locations of addresses,
    business names, and so on.  The output points can be visualized on a map,
    inserted as stops for a route, or loaded as input for a spatial analysis.
    an address, retrieving imagery metadata, or creating a route.

    API Reference: https://developers.arcgis.com/rest/geocode/
    api-reference/geocoding-find.htm
    """

    _PROVIDER = "arcgis"
    _METHOD = "geocode"
    _URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find"
    _RESULT_CLASS = ArcgisResult
    _KEY_MANDATORY = False

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "f": "json",
            "text": location,
            "maxLocations": max_results,
        }

    def _adapt_results(self, json_response):
        return json_response["locations"]

    def _catch_errors(self, json_response):
        status = json_response.get("error")
        if status:
            self.error = status.get("code")
            self.message = status.get("message")
            self.details = status.get("details")

        return self.error


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = ArcgisQuery("Toronto")
    g.debug()
    g = ArcgisQuery("Ottawa, Ontario", max_results=5)
    print(json.dumps(g.geojson, indent=4))
    print([result.address for result in g][:3])
