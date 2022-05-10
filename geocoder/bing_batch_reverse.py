import csv
import io

from geocoder.bing_batch import BingBatch, BingBatchResult


class BingBatchReverseResult(BingBatchResult):
    @property
    def address(self):
        address = self._content
        if address:
            return address[0]

    @property
    def city(self):
        city = self._content
        if city:
            return city[1]

    @property
    def postal(self):
        postal = self._content
        if postal:
            return postal[2]

    @property
    def state(self):
        state = self._content
        if state:
            return state[3]

    @property
    def country(self):
        country = self._content
        if country:
            return country[4]

    @property
    def ok(self):
        return bool(self._content)

    def debug(self, verbose=True):
        with io.StringIO() as output:
            print("\n", file=output)
            print("Bing Batch result\n", file=output)
            print("-----------\n", file=output)
            print(self._content, file=output)

            if verbose:
                print(output.getvalue())

            return [None, None]


class BingBatchReverse(BingBatch):

    method = "batch_reverse"
    _RESULT_CLASS = BingBatchReverseResult

    def generate_batch(self, locations):
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(
            [
                "Id",
                "ReverseGeocodeRequest/Location/Latitude",
                "ReverseGeocodeRequest/Location/Longitude",
                "GeocodeResponse/Address/FormattedAddress",
                "GeocodeResponse/Address/Locality",
                "GeocodeResponse/Address/PostalCode",
                "GeocodeResponse/Address/AdminDistrict",
                "GeocodeResponse/Address/CountryRegion",
            ]
        )

        for idx, location in enumerate(locations):
            writer.writerow(
                [idx, location[0], location[1], None, None, None, None, None]
            )

        return "Bing Spatial Data Services, 2.0\n{}".format(out.getvalue()).encode(
            "utf-8"
        )

    def _adapt_results(self, response):
        # print(type(response))
        result = io.StringIO(response.decode("utf-8"))
        # Skipping first line with Bing header
        next(result)

        rows = {}
        for row in csv.DictReader(result):
            rows[row["Id"]] = [
                row["GeocodeResponse/Address/FormattedAddress"],
                row["GeocodeResponse/Address/Locality"],
                row["GeocodeResponse/Address/PostalCode"],
                row["GeocodeResponse/Address/AdminDistrict"],
                row["GeocodeResponse/Address/CountryRegion"],
            ]

        return rows


if __name__ == "__main__":
    g = BingBatchReverse([(40.7943, -73.970859), (48.845580, 2.321807)], key=None)
    g.debug()
