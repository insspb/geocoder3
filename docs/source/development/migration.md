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

- {func}`geocoder.elevation`
- {func}`geocoder.nokia` - now called as {func}`geocoder.here`
- {func}`geocoder.location` - replaced with {class}`geocoder.Location`, direct class
  sharing
- {func}`geocoder.places`
- {func}`geocoder.reverse`
- {func}`geocoder.timezone`

## Provider's files relocated

All provider's definition files relocated from project main folder to `providers`
module and related subdirectory inside. Directories structure respect provider
implementation function.

If you use direct provider classes imports, please update import statements. If you
use direct helper's functions from `geocoder` module - no changes expected.

## {class}`geocoder.base.OneResult` changes

- Property {attr}`self.raw` renamed to {attr}`self.object_raw_json` to be more
  explainable in inside content. This change affects all subclasses (all providers).
- Property {attr}`self.housenumber` renamed to {attr}`self.house_number`. Affect all
  nested provider's files. Property {attr}`self.house_number` removed and available
  only in concrete provider's implementation.
- Most default properties values replaced from empty string `""` to `None`. Empty
  dicts in some cases left untouched. Please verify properties signatures.
- List of default properties become much smaller, some secondary properties, not
  required to internal {class}`geocoder.base.OneResult` work was removed. This will
  allow new providers faster implementation. Such properties may exist in
  concrete implementations. Removed:
  - {attr}`accuracy`
  - {attr}`quality`
  - {attr}`house_number`
  - {attr}`street`
  - {attr}`city`
  - {attr}`state`
  - {attr}`country`
  - {attr}`postal`
  - {attr}`osm`
  - {attr}`locality`
  - {attr}`province`
  - {attr}`street_number`
  - {attr}`road`
  - {attr}`route`
- All parts of {class}`geocoder.base.OneResult` now have huge docstrings
  and documentation, explaining all behaviour and approach.
- Some internal instance variables and properties renamed to be more concrete. This
  affect all children classes. List of renames:
  - {attr}`json` to {attr}`object_json`

## {class}`geocoder.base.MultipleResultsQuery` changes

- Class will enforce correct setting of {attr}`cls._URL`, {attr}`cls._RESULT_CLASS`,
  {attr}`cls._METHOD`, {attr}`cls._PROVIDER` in nested classes on project
  initialization stage.
- Non-mandatory class variables {attr}`cls.method` and {attr}`cls.provider` renamed
  to {attr}`cls._METHOD`, {attr}`cls._PROVIDER` and become mandatory, related tests
  added.
- Internal class structure changed. Now
  {func}`geocoder.base.MultipleResultsQuery.__init__` does not make an external query,
  and only do object initialization. This allow to initialize any amount of objects
  in advance usage cases (in loops). Query made in
  {func}`geocoder.base.MultipleResultsQuery.__call__` method. This change does not
  change helpers behaviour. I.e. {func}`geocoder.get_results` and related functions
  already respect this change internally.
- Some internal instance variables and properties renamed to be more concrete. This
  affect all children classes. List of renames:
  - {attr}`response` to {attr}`raw_response`
  - {attr}`_list` to {attr}`results_list`
  - {attr}`ok` to {attr}`has_data`
- New instance variables/properties added:
  - {attr}`is_called` - Hold status of external request. I.e. was or not was made.
  - {attr}`raw_json` - Hold unmodified JSON from provider for whole answer.
- Removed functions:
  - {func}`geocoder.base.MultipleResultsQuery.set_default_result`
- {func}`geocoder.base.MultipleResultsQuery.__init__` method now have all default
  keyword arguments in signature, removing silent usage of `kwargs.get("something")`,
  this practice will be extended to all child classes.
- All parts of {class}`geocoder.base.MultipleResultsQuery` now have huge docstrings
  and documentation, explaining all behaviour and approach.

## All print statements replaced with logging module

List of affected files, functions and classes:

- base.py
  - {func}`geocoder.base.OneResult.debug`
  - {func}`geocoder.base.MultipleResultsQuery.debug`
- distance.py
  - {func}`geocoder.distance.haversine` - warnings
- bing_batch.py
  - {func}`geocoder.providers.BingBatchResult.debug`
- bing_batch_forward.py
  - {func}`geocoder.providers.BingBatchForwardResult.debug`
- bing_batch_reverse.py
  - {func}`geocoder.providers.BingBatchReverse.debug`

## Removed(some temporary) project features

- OSM type CLI/Debug output removed as non-well documented

## kwargs approach and naming changes

- There was a confusion between 'deprecated' {attr}`limit` and new {attr}`maxRows`
  provider's setting. All such cases renamed to self-explained {attr}`max_results`.
- Everywhere, where it was possible all {attr}`**kwargs` replaced with complete list of
  function settings, usually with expected input type and defaults, if defaults
  available.

[geocoder]: https://github.com/DenisCarriere/geocoder
[geocoder3]: https://github.com/insspb/geocoder3
[releases]: https://github.com/insspb/geocoder3/releases
[readme.md]: https://github.com/insspb/geocoder3#readme
