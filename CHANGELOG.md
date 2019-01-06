# midea_inventor_dehumidifier Change Log

All notable changes to this project will be documented in this file.

## [1.0.5] - 2019-01-06
### Fixed
- Fixed bug preventing Home Assistant's sensor entity to update current humidity value

## [1.0.4] - 2019-01-06
### Fixed
- Fixed faulty getter methods due to typos for MideaDehumidificationDevice class
### Added
- Implemented send_update_status_command method for MideaClient class
- Added custom_component to support new midea_dehumi platform in Home Assistant 

## [1.0.3] - 2018-12-30
### Added
- Added support for cached device status results
- Added support for invalidSession error (3106)

### Changed
- Changed pycrypto dependency with pycryptodome

## [1.0.2] - 2018-12-29
### Fixed
- Fixed code to support python3

## [1.0.1] - 2018-12-28

- First public release
