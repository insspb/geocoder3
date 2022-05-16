# Testing policy

Testing policy requirements are strict and straightforward:

1. All providers files should be covered with tests.
2. All internet exchange (requests) should be pre-recorded with [vcr.py] and included
   in pull request. This guarantee that tests are connection independent.
3. Main test engine is [pytest].

[pytest]: https://vcrpy.readthedocs.io/en/latest/
[vcr.py]: https://docs.pytest.org/en/
