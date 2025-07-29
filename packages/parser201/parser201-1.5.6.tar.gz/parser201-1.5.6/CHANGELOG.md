# Changelog

<!--------------------------------------------------------------------->

## [1.5.6][1.5.6] - 2025-05-23

### Changed

* Maintenance release to synchronize repository tags.

<!--------------------------------------------------------------------->

## [1.5.5][1.5.5] - 2025-03-06

### Removed

* Drop support for Python 3.8 ([#40][issue40])

<!--------------------------------------------------------------------->

## [1.5.4][1.5.4] - 2025-01-13

### Added

* Implement proper CHANGELOG.md.

### Fixed

* Fix broken pyproject.toml file. ([#38][issue38])

<!--------------------------------------------------------------------->

## 1.5.3 - 2025-11-15

### Changed

* Update dependencies

<!--------------------------------------------------------------------->

## 1.5.2 - 2024-09-23

### Changed

* Migrate packaging and build system to [uv][def2].
* Migrate packaging and build system to [ruff][def3].
* Improve exception handling for invalid date-time objects.
* Migrate documentation generation to [pdoc][def7].

### Fixed

* Code and documentation linting.

<!--------------------------------------------------------------------->

## 1.5.0 - 2024-01-27

### Removed

* Drop support for converting timestamps to local machine time.
  Processing local timezones across multiple architectures and operating
  systems is a bit of a hot mess in Python right now. There's just too
  much variability with regard to OS Settings, location, daylight
  savings time, etc. The performance of this feature was spotty at best.
  There is still support for the _original_ timezone and converstion to
  [_UTC_][def5].

### Fixed

* Clean up packaging for better [PEP561][def4] compliance.
* Clean up type hints.

<!--------------------------------------------------------------------->

## 1.4.1 - 2023-06-22

### Changed

* Migrate code formatter to _black_.

<!--------------------------------------------------------------------->

## 1.4.0 - 2023-04-30

### Changed

### Added

* Add support for access logs that contain both IPv4 and IPv6 addresses.

### Removed

* Dropped support for Python <= 3.7.

### Fixed

* Strengthen regular expression parsing to handle log lines that contain
  a wider array of malicious attacks.
* Code linting and refactoring.

<!--------------------------------------------------------------------->

## 1.3.1 - 2022-10-22

### Changed

* Migrate dependency/build management to [poetry][def6].

<!--------------------------------------------------------------------->

## 1.3.0 - 2022-08-13

### Changed

* Migrated task runner to `make`.

### Added

* Implement `__eq__` magic method for the `LogParser` class. You can
  now perform equality checks on two `LogParser` objects.
* Added test cases for `__eq__`.

### Fixed

* Lint documentation.
* Lint code.

<!--------------------------------------------------------------------->

## 1.2.0 - 2022-07-17

### Changed

* Testing improvements and `pyproject.toml` adjustments for better
  pytest compatability.

### Added

* Implement `__eq__` magic methods in the `FMT` and `TZ` classes.

### Fixed

* Lint documentation.
* Lint code.

<!--------------------------------------------------------------------->

## 1.1.5 - 2022-01-17

### Fixed

* Lint code.

<!--------------------------------------------------------------------->

## 1.1.4 - 2021-12-23

### Fixed

* Lint documentation.

<!--------------------------------------------------------------------->

## 1.1.3 - 2021-12-19

### Added

* Add site logo to README.md.

### Fixed

* Make file tuning.
* Lint documentation.

<!--------------------------------------------------------------------->

## 1.1.0 - 2021-11-13

### Changed

* Migrate API reference to GitHub pages.

### Added

* Implement selectable timestamp conversion options {_original_,
  _local_, [_UTC_][def5]}.
* Implement selectable formatting options for timestamp attribute
  {_string_, _date\_obj_}.

### Fixed

* Lint code.

<!--------------------------------------------------------------------->

## 1.0.2 - 2021-11-05

### Fixed

* Lint documentation.

<!--------------------------------------------------------------------->

## 1.0.0 - 2021-11-04

_Stable production release._

### Changed

* Migrate to a new development framework.

### Fixed

* Use more robust and compartmentalized test cases.
* Lint code.

<!--------------------------------------------------------------------->

## 0.2.0 - 2021-10-31

### Changed

* Change behavior to gracefully fail for any malformed input line. If an
  input line cannot be successfully parsed, all attributes of the
  returned object are set to `None` and no messages are printed.

### Added

* Add additional pytest cases to verify failure behavior.

<!--------------------------------------------------------------------->

## 0.1.9 - 2021-09-15

### Fixed

* Lint code for pep8 compliance.
* Clean up Makefiles and task scripts.

<!--------------------------------------------------------------------->

## 0.1.7 - 2021-06-05

### Changed

* Re-tooled testing scripts to use parameterized test data, and conduct
  more robust testing.

<!--------------------------------------------------------------------->

## 0.1.6 - 2020-12-19

### Fixed

* Address exception handling for initializer input not being a valid
  string data type.
* Lint documentation.

<!--------------------------------------------------------------------->

## 0.1.5 - 2020-10-26

### Changed

* Enabled automatic deployment of tagged releases to pypi from travis
  using encrypted token.
* Convert references to the master branch in the git repository to main
  across the documentation set.

### Added

### Removed

### Fixed

* Lint documentation.

<!--------------------------------------------------------------------->

## 0.1.4 - 2020-10-24

### Added

* Initial pypi release.

### Fixed

* Fix test file filtering issue in `.gitignore`.
* Fix dependencies for travis tests.

<!--------------------------------------------------------------------->

## 0.1.1 - 2020-10-22

### Changed

* Conduct follow-on testing on test.pypi.org.

<!--------------------------------------------------------------------->

## 0.1.0 - 2025-01-11

_Beta release._

<!--------------------------------------------------------------------->

[1.5.4]: https://github.com/geozeke/parser201/releases/tag/v1.5.4
[1.5.5]: https://github.com/geozeke/parser201/releases/tag/v1.5.5
[1.5.6]: https://github.com/geozeke/parser201/releases/tag/v1.5.6
[def2]: https://docs.astral.sh/uv/
[def3]: https://docs.astral.sh/ruff/
[def4]: https://peps.python.org/pep-0561/
[def5]: https://en.wikipedia.org/wiki/Coordinated_Universal_Time
[def6]: https://python-poetry.org/
[def7]: https://github.com/mitmproxy/pdoc
[issue38]: https://github.com/geozeke/parser201/issues/38
[issue40]: https://github.com/geozeke/parser201/issues/40
