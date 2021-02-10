# Colin

![PyPI](https://img.shields.io/pypi/v/colin.svg)
![PyPI - License](https://img.shields.io/pypi/l/colin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colin.svg)
![PyPI - Status](https://img.shields.io/pypi/status/colin.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/427eb0c5dfc040cea798b23575dba025)](https://www.codacy.com/app/user-cont/colin?utm_source=github.com&utm_medium=referral&utm_content=user-cont/colin&utm_campaign=Badge_Grade)
[![Build Status](https://ci.centos.org/job/user-cont-colin-master/badge/icon)](https://ci.centos.org/job/user-cont-colin-master/)

Tool to check generic rules and best-practices for container images and dockerfiles.

For more information, please check our [documentation on colin.readthedocs.io](https://colin.readthedocs.io/en/latest/).

![example](./docs/example.gif)

# Features

- Validate a selected artifact against a ruleset.
- Artifacts can be container images and dockerfiles.
- We provide a default ruleset we believe every container image should satisfy.
- There is a ruleset to validate an artifact whether it complies to [Fedora Container Guidelines](https://fedoraproject.org/wiki/Container:Guidelines)
- Colin can list available rulesets and list checks in a ruleset.
- There is a python API available
- Colin can be integrated into your workflow easily - it can provide results in json format.

## Installation

### Via `pip`

If you are on Fedora distribution, please install python3-pyxattr so you don't
have to compile it yourself when getting it from PyPI.

```bash
$ pip3 install --user colin
```

`colin` is supported on python 3.6+ only.

### On Fedora distribution

colin is packaged in official Fedora repositories:

```
$ dnf install -y colin
```

### Requirements

- For checking `image` target-type, you have to install [podman](https://github.com/containers/libpod/blob/master/docs/tutorials/podman_tutorial.md). If you need to check local docker images, you need to prefix your images with `docker-daemon` (e.g. `colin check docker-daemon:docker.io/openshift/origin-web-console:v3.11`).

- If you want to use `oci` target, you need to install following tools:
  - [umoci](https://github.com/opencontainers/umoci#install)
  - [skopeo](https://github.com/containers/skopeo#skopeo-)

## Usage

```
$ colin --help
Usage: colin [OPTIONS] COMMAND [ARGS]...

  COLIN -- Container Linter

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  check          Check the image/dockerfile (default).
  info           Show info about colin and its dependencies.
  list-checks    Print the checks.
  list-rulesets  List available rulesets.
```

```
$ colin check --help
Usage: colin check [OPTIONS] TARGET

  Check the image/dockerfile (default).

Options:
  -r, --ruleset TEXT           Select a predefined ruleset (e.g. fedora).
  -f, --ruleset-file FILENAME  Path to a file to use for validation (by
                               default they are placed in
                               /usr/share/colin/rulesets).
  --debug                      Enable debugging mode (debugging logs, full
                               tracebacks).
  --json FILENAME              File to save the output as json to.
  --stat                       Print statistics instead of full results.
  -s, --skip TEXT              Name of the check to skip. (this option is
                               repeatable)
  -t, --tag TEXT               Filter checks with the tag.
  -v, --verbose                Verbose mode.
  --checks-path DIRECTORY      Path to directory containing checks (default
                               ['/home/flachman/.local/lib/python3.7/site-
                               packages/colin/checks']).
  --pull                       Pull the image from registry.
  --target-type TEXT           Type of selected target (one of image,
                               dockerfile, oci). For oci, please specify
                               image name and path like this: oci:path:image
  --timeout INTEGER            Timeout for each check in seconds.
                               (default=600)
  --insecure                   Pull from an insecure registry (HTTP or invalid
                               TLS).
  -h, --help                   Show this message and exit.
```

Let's give it a shot:

```
$ colin -f ./rulesets/fedora.json registry.fedoraproject.org/f29/cockpit
PASS:Label 'architecture' has to be specified.
PASS:Label 'build-date' has to be specified.
FAIL:Label 'description' has to be specified.
PASS:Label 'distribution-scope' has to be specified.
:
:
PASS:10 FAIL:8
```

### Directly from git

It's possible to use colin directly from git:

```
$ git clone https://github.com/user-cont/colin.git
$ cd colin
```

We can now run the analysis:

```
$ python3 -m colin.cli.colin -f ./rulesets/fedora.json registry.fedoraproject.org/f29/cockpit
PASS:Label 'architecture' has to be specified.
PASS:Label 'build-date' has to be specified.
FAIL:Label 'description' has to be specified.
PASS:Label 'distribution-scope' has to be specified.
:
:
PASS:10 FAIL:8
```

### Exit codes

Colin can exit with several codes:

- `0` --> OK
- `1` --> error in the execution
- `2` --> CLI error, wrong parameters
- `3` --> at least one check failed
