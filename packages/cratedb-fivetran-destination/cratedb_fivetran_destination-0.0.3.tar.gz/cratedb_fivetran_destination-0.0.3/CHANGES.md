# CrateDB Fivetran Destination Changelog

## Unreleased

## v0.0.3 - 2025-05-23
- Dependencies: Updated to `sqlalchemy-cratedb==0.42.0.dev2`
- Build: Added target to generate `requirements.txt`, and added the generated file
- CI: Stopped building OCI images and standalone artifacts

## v0.0.2 - 2025-05-01
- CLI: Added `--host` option to define on which host to listen on.
  Default: [::]
- Packaging: Improved bootstrapping by supporting directory-based invocation
  per `python src/cratedb_fivetran_destination` and PyInstaller builds per
  `poe build-app`
- Release: Started providing standalone executables on the [releases] page.

## v0.0.1 - 2025-03-31
- Added implementation for `DescribeTable` gRPC method
- Added implementation for `AlterTable` gRPC method
- Type mapping: Mapped `Fivetran.SHORT` to `SQLAlchemy.SmallInteger`
- Type mapping: Mapped `SQLAlchemy.DateTime` to `Fivetran.UTC_DATETIME`
- UI: Removed unneeded form fields. Added unit test.
- CLI: Provided command-line interface for `--port` and `--max-workers` options
- OCI: Provided container image `ghcr.io/crate/cratedb-fivetran-destination`
- Packaging: Removed SDK from repository, build at build-time instead

## v0.0.0 - 2025-02-17
- Added project skeleton
- Added generated SDK gRPC API stubs
- Added example destination blueprint
- Added software integration tests
- DML: Added SQLAlchemy backend implementation for upsert, update, delete
- Connect: Added `url` form field, accepting an SQLAlchemy database connection URL
- Connect: Implemented adapter's `Test` method
- Transform: Fivetran uses special values for designating `NULL` and
  CDC-unmodified values.
- Types: Added support for all Fivetran data types

[releases]: https://github.com/crate/cratedb-fivetran-destination/releases
