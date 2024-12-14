# Changelog

## v6.0.2 (2024-12-14)

### Fix

- attempt #2 to fix Hatch wheel

## v6.0.1 (2024-12-14)

### Fix

- Include pyproject.toml in wheel

## v6.0.0 (2024-12-14)

### Feat

- **deps**: Update flyway/flyway Docker tag to v11

### Fix

- **deps**: update flyway/flyway docker tag to v11.1
- **deps**: update flyway/flyway docker tag to v10.22
- **deps**: update flyway/flyway docker tag to v10.21

## v5.1.0 (2024-10-18)

### Feat

- Support Python 3.13

### Fix

- **deps**: update flyway/flyway docker tag to v10.20
- **deps**: update flyway/flyway docker tag to v10.19
- **deps**: update flyway/flyway docker tag to v10.18

## v5.0.5 (2024-09-01)

### Fix

- Allow creating new files using sqlite repo

## v5.0.4 (2024-09-01)

### Fix

- Don't import PostgresRateLimitingRepo if extra is not installed

## v5.0.3 (2024-09-01)

### Fix

- Make postgres module importable without postgres dependencies

## v5.0.2 (2024-09-01)

### Fix

- Fix digest name for container image merge

## v5.0.1 (2024-09-01)

### Fix

- Correctly set container image name

## v5.0.0 (2024-09-01)

### BREAKING CHANGE

- All repo and policy implementations need to add the *
after their method's self parameters. All invocations that used
positional arguments before will now need to use kw args.
- The added abstract close method on the RateLimitingRepo
will break any existing custom implementations.
- The migrations container image is now called
`rate-limiter-migrations-sqlite`
- The `opentelemetry` extra has been renamed to
`opentelemetry-sqlite3`

### Feat

- Add close method to repos and RateLimiter
- Add Postgres repo

### Fix

- **deps**: update flyway/flyway docker tag to v10.17
- **deps**: update flyway/flyway docker tag to v10.16

## v4.2.1 (2024-06-23)

### Fix

- **deps**: update flyway/flyway docker tag to v10.15
- **deps**: update flyway/flyway docker tag to v10.14
- **deps**: update flyway/flyway docker tag to v10.12

## v4.2.0 (2024-03-10)

### Feat

- Introduce arm64 image

## v4.1.3 (2023-12-30)

### Fix

- Don't pin tzdata

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
