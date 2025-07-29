# CrateDB Fivetran Destination

[![Bluesky][badge-bluesky]][project-bluesky]
[![License][badge-license]][project-license]
[![Release Notes][badge-release-notes]][project-release-notes]
[![Package version][badge-package-version]][project-pypi]
[![Downloads per month][badge-downloads-per-month]][project-downloads]

[![CI][badge-ci]][project-ci]
[![Coverage][badge-coverage]][project-coverage]
[![Status][badge-status]][project-pypi]
[![Supported Python versions][badge-python-versions]][project-pypi]

» [Documentation]
| [Changelog]
| [PyPI]
| [Issues]
| [Source code]
| [License]
| [CrateDB]
| [Community Forum]

## About

[Fivetran] is an automated data movement platform. Automatically, reliably and
securely move data from 650+ sources including SaaS applications, databases,
ERPs, and files to data warehouses, data lakes, and more.

[CrateDB] is a distributed and scalable SQL database for storing and analyzing
massive amounts of data in near real-time, even with complex queries. 
CrateDB is based on Lucene and Elasticsearch, but [compatible with PostgreSQL].

## What's inside

This project and repository provides:

- The source code of the `cratedb-fivetran-destination` package, which implements
  the [CrateDB destination adapter for Fivetran]. It works with both [CrateDB] and
  [CrateDB Cloud].

- The public [issue tracker] for this project. Please use it
  to report problems, and stay informed about their resolutions.

## Status

The status of this software is to be considered work-in-progress,
i.e. pre-alpha.

## Usage

For installation per [PyPI package][PyPI], [OCI image], [standalone executable],
and usage information, please visit the [handbook] document.

For building the application, or hacking on it, please refer to the
[development sandbox] documentation.

## Project Information

### Acknowledgements
Kudos to the authors of all the many software components this library is
inheriting from and building upon.

### Contributing
The CrateDB connector for Fivetran is an open-source project, and is
[managed on GitHub].
Feel free to use the adapter as provided or else modify / extend it
as appropriate for your own applications. We appreciate contributions of any kind.

### License
The project uses the Apache license, like CrateDB itself.


[compatible with PostgreSQL]: https://cratedb.com/docs/guide/feature/postgresql-compatibility/
[CrateDB]: https://cratedb.com/database
[CrateDB Cloud]: https://cratedb.com/database/cloud
[CrateDB destination adapter for Fivetran]: https://cratedb.com/docs/guide/integrate/fivetran/
[development sandbox]: https://github.com/crate/cratedb-fivetran-destination/blob/main/DEVELOP.md
[Fivetran]: https://www.fivetran.com/
[Fivetran SDK Development Guide]: https://github.com/fivetran/fivetran_sdk/blob/main/development-guide.md
[handbook]: https://github.com/crate/cratedb-fivetran-destination/blob/main/docs/handbook.md
[issue tracker]: https://github.com/crate/cratedb-fivetran-destination/issues
[OCI image]: https://github.com/crate/cratedb-fivetran-destination/pkgs/container/cratedb-fivetran-destination
[standalone executable]: https://github.com/crate/cratedb-fivetran-destination/releases

[Changelog]: https://github.com/crate/cratedb-fivetran-destination/blob/main/CHANGES.md
[Community Forum]: https://community.cratedb.com/
[Documentation]: https://cratedb.com/docs/guide/integrate/fivetran/
[Issues]: https://github.com/crate/cratedb-fivetran-destination/issues
[License]: https://github.com/crate/cratedb-fivetran-destination/blob/main/LICENSE
[managed on GitHub]: https://github.com/crate/cratedb-fivetran-destination
[PyPI]: https://pypi.org/project/cratedb-fivetran-destination/
[Source code]: https://github.com/crate/cratedb-fivetran-destination

[badge-bluesky]: https://img.shields.io/badge/Bluesky-0285FF?logo=bluesky&logoColor=fff&label=Follow%20%40CrateDB
[badge-ci]: https://github.com/crate/cratedb-fivetran-destination/actions/workflows/tests.yml/badge.svg
[badge-coverage]: https://codecov.io/gh/crate/cratedb-fivetran-destination/branch/main/graph/badge.svg
[badge-downloads-per-month]: https://pepy.tech/badge/cratedb-fivetran-destination/month
[badge-license]: https://img.shields.io/github/license/crate/cratedb-fivetran-destination.svg
[badge-package-version]: https://img.shields.io/pypi/v/cratedb-fivetran-destination.svg
[badge-python-versions]: https://img.shields.io/pypi/pyversions/cratedb-fivetran-destination.svg
[badge-release-notes]: https://img.shields.io/github/release/crate/cratedb-fivetran-destination?label=Release+Notes
[badge-status]: https://img.shields.io/pypi/status/cratedb-fivetran-destination.svg
[project-bluesky]: https://bsky.app/search?q=cratedb
[project-ci]: https://github.com/crate/cratedb-fivetran-destination/actions/workflows/tests.yml
[project-coverage]: https://app.codecov.io/gh/crate/cratedb-fivetran-destination
[project-downloads]: https://pepy.tech/project/cratedb-fivetran-destination/
[project-license]: https://github.com/crate/cratedb-fivetran-destination/blob/main/LICENSE
[project-pypi]: https://pypi.org/project/cratedb-fivetran-destination
[project-release-notes]: https://github.com/crate/cratedb-fivetran-destination/releases
