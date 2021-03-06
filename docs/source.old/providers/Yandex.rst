Yandex
======

Yandex (Russian: Яндекс) is a Russian Internet company which operates the
largest search engine in Russia with about 60% market share in that country.

The Yandex home page has been rated as the most popular website in Russia.

Geocoding
~~~~~~~~~

.. code-block:: python

    import geocoder

    g = geocoder.yandex('Moscow Russia')
    g.json

This provider may return multiple results by setting the parameter `maxRows` to the desired number (1 by default). You can access those results as described in the page ':doc:`/results`'.

Reverse Geocoding
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import geocoder

    g = geocoder.yandex([55.95, 37.96], method='reverse')
    g.json

Command Line Interface
----------------------

.. code-block:: bash

    $ geocode 'Moscow Russia' --provider yandex --out geojson
    $ geocode '55.95, 37.96' --provider yandex --method reverse

Parameters
----------

- `location`: Your search location you want geocoded.
- `maxRows`: (default=1) Max number of results to fetch
- `lang`: Chose the following language:

    - **ru-RU** — Russian (by default)
    - **uk-UA** — Ukrainian
    - **be-BY** — Belarusian
    - **en-US** — American English
    - **en-BR** — British English
    - **tr-TR** — Turkish (only for maps of Turkey)

- `kind`: Type of toponym (only for reverse geocoding):

    - **house** — house or building
    - **street** — street
    - **metro** — subway station
    - **district** — city district
    - **locality** — locality (city, town, village, etc.)

- `method`: (default=geocode) Use the following:

    - geocode
    - reverse

References
----------

- `Yandex API Reference <http://api.yandex.com/maps/doc/geocoder/desc/concepts/input_params.xml>`_
