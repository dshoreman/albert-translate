# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Fixed
* Syntax updated to support latest version of google-cloud-translate from pip


## [1.0.1] - 2019-09-15
### Fixed
* Compare links in the changelog no longer 404


## [1.0.0] - 2019-06-24
### Added
* Support for setting path to service key file in config
* Ability to translate into multiple comma-separated languages
* Ability to set source language with `from:<code>`
* Hiding of result when source is set to auto and translation matches the
  detected language, as long as there are at least two target languages

### Changed
* Invalid language codes are no longer left for the API to catch
* Options are now added to config automatically with defaults where appropriate

### Fixed
* Now fails gracefully if path to key JSON is missing or invalid


## [0.3.0] - 2019-06-20
### Added
* Ability to open config in editor if config is missing
* New config section for setting default target language
* New *View in Google Translate* action on translations

### Changed
* Subtext now displays language names instead of codes

### Fixed
* Extension no longer shows usage on all non-triggers


## [0.2.0] - 2019-06-19
### Added
* Ability to set target language for translation
* Support for copying translated text to clipboard

### Changed
* Translated text is now used as primary text instead of subtext


## [0.1.0] - 2019-06-18
### Added
* Automatic translation of query into English


[Unreleased]: https://github.com/dshoreman/albert-translate/compare/1.0.1...develop
[1.0.1]: https://github.com/dshoreman/albert-translate/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/dshoreman/albert-translate/compare/0.3.0...1.0.0
[0.3.0]: https://github.com/dshoreman/albert-translate/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/dshoreman/albert-translate/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/dshoreman/albert-translate/releases/tag/0.1.0
