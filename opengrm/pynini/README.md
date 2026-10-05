# Pynini: Grammar compilation in Python

        ,ggggggggggg,
       dP"""88""""""Y8,
       Yb,  88      `8b
        `"  88      ,8P                        gg                  gg
            88aaaad8P"                         ""                  ""
            88"""""  gg     gg   ,ggg,,ggg,    gg    ,ggg,,ggg,    gg
            88       I8     8I  ,8" "8P" "8,   88   ,8" "8P" "8,   88
            88       I8,   ,8I  I8   8I   8I   88   I8   8I   8I   88
            88      ,d8b, ,d8I ,dP   8I   Yb,_,88,_,dP   8I   Yb,_,88,_
            88      P""Y88P"8888P'   8I   `Y88P""Y88P'   8I   `Y88P""Y8
                          ,d8I'
                        ,dP'8I
                       ,8"  8I
                       I8   8I
                       `8, ,8I
                        `Y8P"

## Getting started

To get started, see [the docs](docs/index.md).

For some more context, see
[How to get superior text processing in Python with Pynini](https://www.oreilly.com/ideas/how-to-get-superior-text-processing-in-python-with-pynini)
and
[Pynini: A Python library for weighted finite-state grammar compilation](http://openfst.cs.nyu.edu/twiki/pub/GRM/Pynini/pynini-paper.pdf).

## CI wheels

Every push to `main` builds a CPython 3.12 Linux x86-64 wheel with Bazel. The
wheel is available under the **Artifacts** section of that commit's **Pynini
wheels** Actions run. Download the artifact, unzip it, and install the wheel
with `python -m pip install path/to/opengrm_pynini-*.whl` using CPython 3.12.
The installed module is imported as `from opengrm.pynini import pynini`.

The same wheel is also stored in GitHub Packages as a GHCR container image
tagged `ghcr.io/OWNER/REPO/pynini-wheels:sha-COMMIT_SHA`. For example, after
`docker pull`, use `docker create` and `docker cp CONTAINER:/wheels/. ./wheels/`
to copy the wheel out of the image. GitHub Packages has no Python package
registry, so the GHCR package stores the wheel file rather than serving a pip
index. Actions artifacts follow the repository's artifact retention policy;
the SHA-tagged GHCR package provides a persistent copy.
