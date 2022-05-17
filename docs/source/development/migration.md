# Geocoder to geocoder3 migration

During initial migration of [geocoder] project to [geocoder3] many changes in
structure and approach was made. Here is list of noticeable changes, that should be
considered during migration from [geocoder] to [geocoder3]. Also, please read changes
in described in project [releases] section.

Some parts of text below describe new provider's approach. This is valid only to
providers, that are marked as **Geocoder3 ready** in main [readme.md] file.

## Default geocoding engine changed from Google to OpenStreetMap

As Google engine now requires mandatory API key, default engine changed to free
OpenStreetMap.

## Some helper functions removed from `api.py` and project

Functions for 'silence' geocoding or IP geocoding are removed from project. Please
use exact provider and provider configuration for such requests. Functions itself
located in `api.py`.

List of removed functions:

- `geocoder.elevation`
- `geocoder.nokia` - now called as `geocoder.here`
- `geocoder.location` - replaced with `geocoder.Location`, direct class sharing
- `geocoder.places`
- `geocoder.reverse`
- `geocoder.timezone`

## Provider's files relocated

All providers definition files relocated from project main folder to `providers`
module and related subdirectory inside. Directories structure respect provider
implementation function.

If you use direct provider classes imports, please update import statements. If you
use direct helper's functions from `geocoder` module - no changes needed.

## base.py `OneResult` changes

- Property `self.raw` renamed to `self.raw_json` to be more explainable in inside
  content. This change affects all subclesses (all providers).
- Property `self.housenumber` renamed to `self.house_number`. Affect all nested
  provider's files.
- All default properties values replaced from empty string `""` to `None`. Empty
  dicts in some cases left untouched. Please verify properties signatures.

## All print statements replaced with logging module

List of affected files, functions and classes:

- `base.py`
  - `OneResult.debug()`
  - `MultipleResultsQuery.debug()`
- `distance.py`
  - `haversine()` - warnings
- `bing_batch.py`
  - `BingBatchResult.debug()`
- `bing_batch_forward.py`
  - `BingBatchForwardResult.debug()`
- `bing_batch_reverse.py`
  - `BingBatchReverse.debug()`

## kwargs approach and naming changes

- There was a confusion between 'deprecated' `limit` and new `maxRows` provider's
  setting. All such cases renamed to self-explained `max_results`.
- Everywhere, where it was possible all `**kwargs` replaced with complete list of
  function settings, usually with expected input type and defaults, if defaults
  available.

[geocoder]: https://github.com/DenisCarriere/geocoder
[geocoder3]: https://github.com/insspb/geocoder3
[releases]: https://github.com/insspb/geocoder3/releases
[readme.md]: https://github.com/insspb/geocoder3#readme
