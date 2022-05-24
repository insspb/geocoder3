__all__ = ["IpfinderQuery", "IpfinderResult"]

import logging

from geocoder.base import MultipleResultsQuery, OneResult


class IpfinderResult(OneResult):
    @property
    def status(self):
        return self.object_raw_json.get("status")

    @property
    def status_message(self):
        return self.object_raw_json.get("status_message")

    @property
    def ip(self):
        return self.object_raw_json.get("ip")

    @property
    def type(self):
        return self.object_raw_json.get("type")

    @property
    def continent_code(self):
        return self.object_raw_json.get("continent_code")

    @property
    def continent_name(self):
        return self.object_raw_json.get("continent_name")

    @property
    def country_code(self):
        return self.object_raw_json.get("country_code")

    @property
    def country_name(self):
        return self.object_raw_json.get("country_name")

    @property
    def country_native_name(self):
        return self.object_raw_json.get("country_native_name")

    @property
    def region_name(self):
        return self.object_raw_json.get("region_name")

    @property
    def city(self):
        return self.object_raw_json.get("city")

    @property
    def latitude(self):
        return self.object_raw_json.get("latitude")

    @property
    def longitude(self):
        return self.object_raw_json.get("longitude")

    @property
    def capital(self):
        return self.object_raw_json.get("location", {}).get("capital")

    @property
    def country_flag(self):
        return self.object_raw_json.get("location", {}).get("country_flag")

    @property
    def flag_png(self):
        return self.object_raw_json.get("location", {}).get("flag_png")

    @property
    def country_flag_emoji(self):
        return self.object_raw_json.get("location", {}).get("country_flag_emoji")

    @property
    def country_flag_emoji_unicode(self):
        return self.object_raw_json.get("location", {}).get(
            "country_flag_emoji_unicode"
        )

    @property
    def calling_code(self):
        return self.object_raw_json.get("location", {}).get("calling_code")

    @property
    def toplevel_domain(self):
        return self.object_raw_json.get("location", {}).get("toplevel_domain")

    @property
    def alpha3_code(self):
        return self.object_raw_json.get("location", {}).get("alpha3_code")

    @property
    def population(self):
        return self.object_raw_json.get("location", {}).get("population")

    @property
    def is_eu(self):
        return self.object_raw_json.get("location", {}).get("is_eu")

    @property
    def is_ar(self):
        return self.object_raw_json.get("location", {}).get("is_ar")

    @property
    def time_zone_id(self):
        return self.object_raw_json.get("time_zone", {}).get("id")

    @property
    def time_zone_utc(self):
        return self.object_raw_json.get("time_zone", {}).get("UTC")

    @property
    def time_zone_gmt_offset(self):
        return self.object_raw_json.get("time_zone", {}).get("gmt_offset")

    @property
    def time_zone_current_time(self):
        return self.object_raw_json.get("time_zone", {}).get("current_time")

    @property
    def currency_name(self):
        return self.object_raw_json.get("currency", {}).get("name")

    @property
    def currency_symbol(self):
        return self.object_raw_json.get("currency", {}).get("symbol")

    @property
    def currency_symbol_native(self):
        return self.object_raw_json.get("currency", {}).get("symbol_native")

    @property
    def languages_code(self):
        return self.object_raw_json.get("languages", {}).get("code")

    @property
    def languages_name(self):
        return self.object_raw_json.get("languages", {}).get("name")

    @property
    def languages_name_native(self):
        return self.object_raw_json.get("languages", {}).get("name_native")

    @property
    def connection_asn(self):
        return self.object_raw_json.get("connection", {}).get("asn")

    @property
    def connection_organization(self):
        return self.object_raw_json.get("connection", {}).get("organization")

    @property
    def connection_domain(self):
        return self.object_raw_json.get("connection", {}).get("domain")

    @property
    def connection_type(self):
        return self.object_raw_json.get("connection", {}).get("type")

    @property
    def is_proxy(self):
        return self.object_raw_json.get("security", {}).get("is_proxy")

    @property
    def proxy_type(self):
        return self.object_raw_json.get("security", {}).get("proxy_type")

    @property
    def is_tor(self):
        return self.object_raw_json.get("security", {}).get("is_tor")

    @property
    def is_spam(self):
        return self.object_raw_json.get("security", {}).get("is_spam")

    @property
    def threat_level(self):
        return self.object_raw_json.get("security", {}).get("threat_level")


class IpfinderQuery(MultipleResultsQuery):
    """
    IPFinder REST Services

    IP address details (city, region, country, postal code, latitude and more ..).
    ASN details (Organization name, registry,domain,company_type, and more .. ).
    Firewall by supported formats details (apache_allow, nginx_deny, CIDR, and more ..)
    IP Address Ranges by the Organization name details (list_asn, list_prefixes,
    and more ..).
    service status details (queriesPerDay, queriesLeft, key_type, key_info).
    Get Domain IP (asn, organization,country_code ....).
    Get Domain IP history (total_ip, list_ip,organization,asn ....).
    Get list Domain By ASN, Country,Ranges (select_by , total_domain , list_domain ..).

    API Reference      : https://ipfinder.io/docs
    Get IPFinder key   : https://ipfinder.io/auth/signup
    """

    _PROVIDER = "ipfinder"
    _METHOD = "geocode"
    _URL = "http://api.ipfinder.io/v1/"
    _RESULT_CLASS = IpfinderResult
    _KEY_MANDATORY = False

    def _build_params(self, location=None, provider_key=None, **kwargs):

        if location is None:
            self.url = "https://api.ipfinder.io/v1/"
        else:
            self.url = "https://api.ipfinder.io/v1/{0}".format(self.location)

        self.provider_key = "free" if provider_key is None else provider_key

        return {"token": self.provider_key, "format": "json"}

    def _build_headers(self, provider_key, **kwargs):
        return {"user-agent": "geocoder Python-client"}

    def _adapt_results(self, json_response):
        return [json_response]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = IpfinderQuery("8.8.8.8")
    g.debug()
