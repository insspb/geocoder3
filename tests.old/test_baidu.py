import geocoder

location = "兆维华灯大厦,北京"
city = "北京"
place = (39.9789660352, 116.497157786)


def test_baidu():
    """Expected result :
    http://api.map.baidu.com/geocoder/v2/?callback=renderOption&output=json&address=百度大厦&city=北京市&ak=<Your API Key>   # noqa
    """
    g = geocoder.baidu(location, key="35d0b72b3e950e5d0b74b037262f8b41")
    assert g.ok
    osm_count, fields_count = g.debug()[0]
    assert osm_count == 0
    assert fields_count >= 7


def test_baidu_reverse():
    """Expected result:
    http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=39.9789660352,116.497157786&output=json&pois=1&ak=<Your API Key> # noqa
    """
    g = geocoder.baidu(place, method="reverse", key="35d0b72b3e950e5d0b74b037262f8b41")
    assert g.ok
    assert g.country == "中国"
    assert g.state == "北京市"
    assert g.city == "北京市"
    assert g.street == "酒仙桥路"
