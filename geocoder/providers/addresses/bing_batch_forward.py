__all__ = ["BingBatchForward"]

import csv
import io
import logging

from geocoder.providers.addresses.bing_batch import BingBatch, BingBatchResult

logger = logging.getLogger(__name__)


class BingBatchForwardResult(BingBatchResult):
    @property
    def lat(self):
        coord = self._content
        if coord:
            return float(coord[0])

    @property
    def lng(self):
        coord = self._content
        if coord:
            return float(coord[1])

    @property
    def ok(self):
        return bool(self._content)

    def debug(self):
        logger.debug("Bing Batch result")
        logger.debug("-----------")
        logger.debug(self._content)

        return [None, None]


class BingBatchForward(BingBatch):
    _METHOD = "batch"
    _RESULT_CLASS = BingBatchForwardResult

    def generate_batch(self, addresses):
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(
            [
                "Id",
                "GeocodeRequest/Query",
                "GeocodeResponse/Point/Latitude",
                "GeocodeResponse/Point/Longitude",
            ]
        )

        for idx, address in enumerate(addresses):
            writer.writerow([idx, address, None, None])

        return "Bing Spatial Data Services, 2.0\n{}".format(out.getvalue()).encode(
            "utf-8"
        )

    def _adapt_results(self, response):
        result = io.StringIO(response.decode("utf-8"))
        # Skipping first line with Bing header
        next(result)

        rows = {}
        for row in csv.DictReader(result):
            rows[row["Id"]] = [
                row["GeocodeResponse/Point/Latitude"],
                row["GeocodeResponse/Point/Longitude"],
            ]

        return rows


if __name__ == "__main__":
    g = BingBatchForward(["Denver,CO", "Boulder,CO"], key=None)
    g.debug()
