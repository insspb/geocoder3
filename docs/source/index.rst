[WIP] Geocoder3: Simple, Consistent
===================================

Release v\ |version|.

Simple and consistent geocoding library written in Python.

Many online providers such as Google & Bing have geocoding services,
these providers do not include Python libraries and have different
JSON responses between each other.

It can be very difficult sometimes to parse a particular geocoding provider
since each one of them have their own JSON schema.

Here is a typical example of retrieving a Lat & Lng from Google using Python,
things shouldn't be this hard.

.. code-block:: python

    import requests
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': 'Mountain View, CA'}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    location['lat'], location['lng']
    # (37.3860517, -122.0838511)

Now lets use Geocoder to do the same task.

.. code-block:: python

    import geocoder
    g = geocoder.google('Mountain View, CA')
    g.latlng
    # (37.3860517, -122.0838511)

API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
    :maxdepth: 3

    features/index
    providers/index
    api/index

Contributor Guide
-----------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
    :maxdepth: 3

    development/index
