__all__ = ["GeonamesChildren"]

from geocoder.providers.addresses.geonames import GeonamesQuery


class GeonamesChildren(GeonamesQuery):
    """Children:
    http://api.geonames.org/childrenJSON?formatted=true&geonameId=6094817
    """

    _PROVIDER = "geonames"
    _METHOD = "children"

    _URL = "http://api.geonames.org/childrenJSON"

    def _build_params(self, location, provider_key, **kwargs):
        """Will be overridden according to the targetted web service"""
        return {
            "geonameId": location,
            "username": provider_key,
        }


if __name__ == "__main__":
    print("Searching Ottawa...")
    g = GeonamesQuery("Ottawa, Ontario")
    g.debug()
    print("Searching its children...")
    c = GeonamesChildren(g.pop().geonames_id)
    c.debug()
