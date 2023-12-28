# Changelog

## v4.1.2 (2023-12-28)

### Fix

- **otel**: Use return value of instrument_connection

## v4.1.1 (2023-12-28)

### Fix

- Log info if sqlite is not instrumented

## v4.1.0 (2023-12-28)

### Feat

- Start new otel span for top-level RateLimiter methods
- Add optional OpenTelemetry instrumentation

## v4.0.0 (2023-11-10)

### BREAKING CHANGE

- This version changes the pip package name to
prep-rate-limiter and the Python package name to rate_limiter.

## v3.0.0 (2023-11-10)

### BREAKING CHANGE

- This release drops support for Python 3.10

### Fix

- Add migration location explicitly to config

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
