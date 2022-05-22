__all__ = ["GeonamesHierarchy"]

from geocoder.providers.addresses.geonames_children import GeonamesChildren


class GeonamesHierarchy(GeonamesChildren):
    """Hierarchy:
    http://api.geonames.org/hierarchyJSON?formatted=true&geonameId=6094817
    """

    _PROVIDER = "geonames"
    _METHOD = "hierarchy"

    _URL = "http://api.geonames.org/hierarchyJSON"


if __name__ == "__main__":
    print("Searching Ottawa's hierarchy...")
    c = GeonamesHierarchy(6094817)
    c.debug()
