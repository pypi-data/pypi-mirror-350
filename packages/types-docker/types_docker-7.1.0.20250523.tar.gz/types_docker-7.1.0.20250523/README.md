## Typing stubs for docker

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`docker`](https://github.com/docker/docker-py) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `docker`. This version of
`types-docker` aims to provide accurate annotations for
`docker==7.1.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/docker`](https://github.com/python/typeshed/tree/main/stubs/docker)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.400,
and pytype 2024.10.11.
It was generated from typeshed commit
[`23e702b4b113cbbb2a5bd3415a707b7760945978`](https://github.com/python/typeshed/commit/23e702b4b113cbbb2a5bd3415a707b7760945978).