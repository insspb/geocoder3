# Base provider definition

Base classes of provider definition responsible for minimum set of methods and
properties, that should be implemented or overridden in all nested providers.

This set of methods and properties guarantees working of all project [features] and
minimum similarity of result of any provider usage.

Each provider itself can extend supported and extracted properties, available in
direct instance access. For list of such extracted properties please read
documentation for exact provider.

## Base Multiple Results Query class

```{eval-rst}
.. autoclass:: geocoder.base.MultipleResultsQuery
   :members:  
   :exclude-members: insert, add
   :undoc-members:
   :special-members: __init__, __init_subclass__, __getattr__, __call__
   :private-members: _get_api_key, _build_headers, _build_params, _before_initialize,
        _initialize, _connect, _adapt_results, _parse_results, _catch_errors
```

## Base One Result class

```{eval-rst}
.. autoclass:: geocoder.base.OneResult
   :members:
   :undoc-members:
   :special-members: __init__
   :private-members: _parse_json_with_fieldnames, _get_bbox
```

[features]: ../features/index.rst
