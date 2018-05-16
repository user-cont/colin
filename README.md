# Colin

![PyPI](https://img.shields.io/pypi/v/colin.svg)
![PyPI - License](https://img.shields.io/pypi/l/colin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colin.svg)
![PyPI - Status](https://img.shields.io/pypi/status/colin.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/427eb0c5dfc040cea798b23575dba025)](https://www.codacy.com/app/user-cont/colin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=user-cont/colin&amp;utm_campaign=Badge_Grade)

Tool to check generic rules/best-practices for containers/images/dockerfiles.

Initial plan is to validate containers/images/dockerfiles against different ecosystems:
 - Red Hat Container Catalogue
 - Fedora Infrastructure (and [Fedora Container Guidelines](https://fedoraproject.org/wiki/Container:Guidelines))
 - Project Atomic [Container Best Practices](http://docs.projectatomic.io/container-best-practices/)

*Colin* will also provide generic checks for maintainers or users of containerized content.

For more information, please check our [documentation on colin.readthedocs.io](https://colin.readthedocs.io/en/latest/).

![example](./docs/example.gif)


## Installation


### Via `pip`

If you are on Fedora distribution, please install python3-pyxattr so you don't have to compile yourself when getting it from PyPI.

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
  check          Check the image/container (default).
  list-checks    Print the checks.
  list-rulesets  List available rulesets.
```

```
$ colin check -h
Usage: colin check [OPTIONS] TARGET

  Check the image/container (default).

Options:
  -r, --ruleset TEXT           Select a predefined ruleset (e.g. fedora).
  -f, --ruleset-file FILENAME  Path to a file to use for validation (by
                               default they are placed in /usr/share/colin).
  --debug                      Enable debugging mode (debugging logs, full
                               tracebacks).
  --json FILENAME              File to save the output as json to.
  -s, --stat                   Print statistics instead of full results.
  -v, --verbose                Verbose mode.
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

We can also check containers:
```
$ docker run --name some-fedora -d fedora sleep 300
$ colin -f ./rulesets/default.json some-fedora
LABELS:
FAIL:Label 'maintainer' has to be specified.
FAIL:Label 'name' has to be specified.
...
$ docker run --name my-fedora -l maintainer=myname -d fedora sleep 300
# Adding maintainer name fixes the check:
$ colin -f ./rulesets/default.json  my-fedora
LABELS:
PASS:Label 'maintainer' has to be specified.
FAIL:Label 'name' has to be specified.
...
```

### How to test a container image and Dockerfile with Colin locally

We provide a simple Ansible playbook which you can put inside your CI system and use colin in there. It installs and executes colin.

```bash
make check-local -e TEST_IMAGE_NAME=<image_name> -e ANSIBLE_EXTRA_ARGS=-vv -e RULESET=fedora -e ARTIFACTS_DIR=<directory_for_results> -e RESULTS=<result_file>  -e setup=true
```

The makefile target above executes the playbook like this:

```bash
ansible-playbook $(ANSIBLE_EXTRA_ARGS) -e ruleset=$(RULESET) -e subject=$(TEST_IMAGE_NAME) -e results=$(RESULTS) -e artifacts_dir=$(ARTIFACTS_DIR) ./local.yml -e setup=true
```

Description of the parameters:
- `TEST_IMAGE_NAME` — name of the image to check.
- `ANSIBLE_EXTRA_ARGS` — extra arguments for `ansible-playbook` command.
- `RULESET` — name of ruleset to use. By default it's `fedora` ruleset.
- `ARTIFACTS_DIR` — directory where the results are stored. Ansible playbook creates it if needed. By default `./artifacts`.
- `RESULTS` — filename which is being used by `colin` for storing results. By default `colin.json`.

E.g. checking `fedora:27` image with ruleset `fedora` and stored results `colin.json` into directory `artifacts`:

```bash
make check-local -e TEST_IMAGE_NAME=fedora:27 -e RULESET=fedora -e ARTIFACTS_DIR=./artifacts
```


### Directly from git

It's possible to use colin directly from git:

```
$ git clone https://github.com/user-cont/colin.git
$ cd colin
$ python3 -m colin.cli.colin -h
Usage: colin [OPTIONS] COMMAND [ARGS]...

  COLIN -- Container Linter

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  check          Check the image/container (default).
  list-checks    Print the checks.
  list-rulesets  List available rulesets.
```

We can now run the analysis:

```
$ python3 -m colin.cli.colin -f ./rulesets/fedora.json fedora:27
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
WARN:Label 'vcs-type' has to be specified.
WARN:Label 'description' has to be specified.
WARN:Label 'io.k8s.description' has to be specified.
WARN:Label 'vcs-url' has to be specified.
WARN:Label 'maintainer' has to be specified.
WARN:Label 'io.openshift.expose-services' has to be specified.
...
```

### Exit codes

Colin can exit with several codes:

- `0` --> OK
- `1` --> error in the execution
- `2` --> CLI error, wrong parameters
- `3` --> at least one check failed

## Technical details

![Scheme](./docs/scheme.png)
