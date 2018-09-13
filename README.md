# Colin

![PyPI](https://img.shields.io/pypi/v/colin.svg)
![PyPI - License](https://img.shields.io/pypi/l/colin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colin.svg)
![PyPI - Status](https://img.shields.io/pypi/status/colin.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/427eb0c5dfc040cea798b23575dba025)](https://www.codacy.com/app/user-cont/colin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=user-cont/colin&amp;utm_campaign=Badge_Grade)
[![Build Status](https://ci.centos.org/job/user-cont-colin-master/badge/icon)](https://ci.centos.org/job/user-cont-colin-master/)

Tool to check generic rules and best-practices for container images and dockerfiles.

For more information, please check our [documentation on colin.readthedocs.io](https://colin.readthedocs.io/en/latest/).

![example](./docs/example.gif)


# Features

* Validate a selected artifact against a ruleset.
* Artifacts can be container images and dockerfiles.
* We provide a default ruleset we believe every container image should satisfy.
* There is a ruleset to validate an artifact whether it complies to [Fedora Container Guidelines](https://fedoraproject.org/wiki/Container:Guidelines)
* Colin can list available rulesets and list checks in a ruleset.
* There is a python API available
* Colin can be integrated into your workflow easily - it can provide results in json format.


## Installation


### Via `pip`

If you are on Fedora distribution, please install python3-pyxattr so you don't
have to compile it yourself when getting it from PyPI.

```bash
$ pip3 install --user colin
```


### On Fedora distribution

colin is packaged in official Fedora repositories:
```
$ dnf install -y colin
```


## Usage

```
$ colin -h
Usage: colin [OPTIONS] COMMAND [ARGS]...

  COLIN -- Container Linter

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  check          Check the image/dockerfile (default).
  list-checks    Print the checks.
  list-rulesets  List available rulesets.
```

```
$ colin check -h
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
  -s, --stat                   Print statistics instead of full results.
  -t, --tag TEXT               Filter checks with the tag.
  -v, --verbose                Verbose mode.
  --checks-path DIRECTORY      Path to directory containing checks (default
                               ['/home/flachman/.local/lib/python3.6/site-
                               packages/colin/checks']).
  --pull                       Pull the image from registry.
  --target-type TEXT           Type of selected target (one of image,
                               dockerfile, ostree). For ostree,
                               please specify image name and path like this:
                               image@path
  --insecure                   Pull from an insecure registry (HTTP or invalid
                               TLS).
  -h, --help                   Show this message and exit.
```

Let's give it a shot:
```
$ colin -f ./rulesets/fedora.json fedora:27
LABELS:
FAIL:Label 'maintainer' has to be specified.
PASS:Label 'name' has to be specified.
FAIL:Label 'com.redhat.component' has to be specified.
FAIL:Label 'summary' has to be specified.
PASS:Label 'version' has to be specified.
FAIL:Label 'usage' has to be specified.
FAIL:Label 'release' has to be specified.
FAIL:Label 'architecture' has to be specified.
WARN:Label 'url' has to be specified.
WARN:Label 'help' has to be specified.
WARN:Label 'build-date' has to be specified.
WARN:Label 'distribution-scope' has to be specified.
WARN:Label 'vcs-ref' has to be specified.
...
```


### Directly from git

It's possible to use colin directly from git:

```
$ git clone https://github.com/user-cont/colin.git
$ cd colin
```

We can now run the analysis:

```
$ python3 -m colin.cli.colin -f ./rulesets/fedora.json fedora:27
FAIL:Label 'architecture' has to be specified.
FAIL:Label 'build-date' has to be specified.
FAIL:Label 'description' has to be specified.
FAIL:Label 'distribution-scope' has to be specified.
FAIL:Label 'help' has to be specified.
FAIL:Label 'io.k8s.description' has to be specified.
FAIL:Label 'url' has to be specified.
FAIL:Label 'vcs-ref' has to be specified.
FAIL:Label 'vcs-type' has to be specified.
FAIL:Label 'vcs-url' has to be specified.
FAIL:Label 'com.redhat.component' has to be specified.
FAIL:Label 'maintainer' has to be specified.
FAIL:Label 'name' has to be specified.
FAIL:Label 'release' has to be specified.
FAIL:Label 'summary' has to be specified.
FAIL:Label 'version' has to be specified.
FAIL:Cmd or Entrypoint has to be specified
ERROR:The 'helpfile' has to be provided.
FAIL:Service should not run as root by default.
FAIL:Label 'usage' has to be specified.

FAIL:21 ERROR:1
```

### Exit codes

Colin can exit with several codes:

- `0` --> OK
- `1` --> error in the execution
- `2` --> CLI error, wrong parameters
- `3` --> at least one check failed
