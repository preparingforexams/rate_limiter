# Changelog

## 2.1.0

### Features

- Add default CMD to migration image (`flyway migrate -skipCheckForUpdate`)
- Updated to Flyway 10

## 2.0.1

### Fixed

- Never create timezone-naive datetimes

## 2.0.0

### Breaking Changes

- Dropped Python 3.9 support
- Removed dependency on pendulum
  - This means the type `pendulum.DateTime` has been replaced by a `datetime.datetime` everywhere

### New

- Added Python 3.12 support
