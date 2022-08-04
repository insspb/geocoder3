import json

import requests_mock

import geocoder

location = "Ottawa, Ontario"
city = "Ottawa"
country = "Canada"
ottawa = (45.421106, -75.690308)


def test_locationiq():
    url = "https://locationiq.org/v1/search.php?q=Ottawa%2C+Ontario&format=json&key=TEST_KEY"  # noqa
    data_file = "tests/results/locationiq.json"
    with requests_mock.Mocker() as mocker, open(data_file, "r") as ip:
        mocker.get(url, text=ip.read())
        g = geocoder.locationiq(location, key="TEST_KEY")
        assert g.has_data
        assert g[0].lat == ottawa[0]
        assert g[0].lng == ottawa[1]


def test_locationiq_single_result():
    url = "https://locationiq.org/v1/search.php?q=Ottawa%2C+Ontario&format=json&limit=1&key=TEST_KEY"  # noqa
    data_file = "tests/results/locationiq.json"
    with requests_mock.Mocker() as mocker, open(data_file, "r") as ip:
        mock_result = json.loads(ip.read())
        single_mock_result = json.dumps(mock_result[:1])
        mocker.get(url, text=single_mock_result)
        g = geocoder.locationiq(location, key="TEST_KEY", max_results=1)
        assert g.has_data
        assert len(g) == 1


def test_locationiq_multi_result():
    url = "https://locationiq.org/v1/search.php?q=Ottawa%2C+Ontario&format=json&key=TEST_KEY"  # noqa
    data_file = "tests/results/locationiq.json"
    with requests_mock.Mocker() as mocker, open(data_file, "r") as ip:
        mocker.get(url, text=ip.read())
        g = geocoder.locationiq(location, key="TEST_KEY")
        assert g.has_data
        assert len(g) > 1


def test_locationiq_reverse():
    url = "https://locationiq.org/v1/reverse.php?format=json&key=TEST_KEY&lat=45.421106&lon=-75.690308"  # noqa
    data_file = "tests/results/locationiq_reverse.json"
    with requests_mock.Mocker() as mocker, open(data_file, "r") as ip:
        mocker.get(url, text=ip.read())
        g = geocoder.locationiq(
            f"{ottawa[0]}, {ottawa[1]}", key="TEST_KEY", method="reverse"
        )

        assert g.has_data
        assert g.city == city
        assert g.country == country
