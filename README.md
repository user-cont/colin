![PyPI](https://img.shields.io/pypi/v/colin.svg)
![PyPI - License](https://img.shields.io/pypi/l/colin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colin.svg)
![PyPI - Status](https://img.shields.io/pypi/status/colin.svg)

# Colin

Tool to check generic rules/best-practices for containers/images/dockerfiles.

Initial plan is to validate containers/images/dockerfiles against different ecosystems:
 - Red Hat Container Catalogue
 - Fedora Infra (and container guidelines)
 - CentOS
 - Atomic Container Best Practices

*Colin* will also provide generic checks for maintainers or users of containerized content.

For more information, please check our [documentation on colin.readthedocs.io](https://colin.readthedocs.io/en/latest/).

![example](./docs/example.gif)


## Usage

### How to test a container image and Dockerfile with Colin locally

```bash
    make check-local -e TEST_IMAGE_NAME=<image_name> -e ANSIBLE_EXTRA_ARGS=-vv -e CONFIG=<config_file> -e ARTIFACTS_DIR=<directory_for_results> -e RESULTS=<result_file>  -e setup=true
```

which runs ansible playbook, by a command:

```bash
    ansible-playbook $(ANSIBLE_EXTRA_ARGS) -e config=$(CONFIG) -e subject=$(TEST_IMAGE_NAME) -e results=$(RESULTS) -e artifacts_dir=$(ARTIFACTS_DIR) ./local.yml -e setup=true
```

The parameters used in command specify:
- TEST_IMAGE_NAME ... name of the image which colin tests
- ANSIBLE_EXTRA_ARGS ... extra arguments for ansible command
- CONFIG ... name of default configuration file which is being used. By default `fedora`
- ARTIFACTS_DIR ... directory where the results are stored. Ansible playbook creates it if needed. By default `./artifacts`
- RESULTS ... filename which is being used by `colin` for storing results. By default `colin.json`

E.g. checking `fedora:27` image with ruleset `fedora` and stored results `colin.json` into directory `artifacts`:

```bash
make check-local -e TEST_IMAGE_NAME=fedora:27 -e CONFIG=fedora -e ARTIFACTS_DIR=./artifacts
```

### Installing via `pip`


```bash
$ pip3 install --user colin
```

> If you are on Fedora distribution, please install python3-pyxattr so you don't have to compile yourself when getting it from PyPI.

This is how you can use colin afterwards:

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


### Directly from git

Once you clone colin locally, you can invoke it directly from cloned git repository:

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

*Colin* will be available as a Python API, and will provide command line interface so you can easily use it locally.

Each ecosystem will define a set of checks to validate the artifacts. Checks will have different severity level so that we can classify checks as required or optional.

![Scheme](./docs/scheme.png)

## TODO

- [ ] support Fedora infrastructure ([see issue about GSoC project for more information](https://github.com/user-cont/colin/issues/3))
