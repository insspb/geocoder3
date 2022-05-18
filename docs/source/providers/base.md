# Base provider definition

Base classes of provider definition responsible for minimum set of methods and
properties, that should be implemented or overridden in all nested providers.

This set of methods and properties guarantees working of all project [features] and
minimum similarity of result of any provider usage.

Each provider itself can extend supported and extracted properties, available in
direct instance access. For list of such extracted properties please read
documentation for exact provider.

## Base result class

```{eval-rst}
.. autoclass:: geocoder.base.OneResult
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
```

## Base query class

```{eval-rst}
.. autoclass:: geocoder.base.MultipleResultsQuery
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
```
