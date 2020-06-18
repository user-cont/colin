# Contributing Guidelines

Thanks for your interest in contributing to `colin`.

The following is a set of guidelines for contributing to `colin`.
Use your best judgement, and feel free to propose changes to this document in a pull request.

By contributing to this project you agree to the Developer Certificate of Origin (DCO). This document is a simple statement that you, as a contributor, have the legal right to submit the contribution. See the [DCO](DCO) file for details.

## Reporting Bugs
Before creating bug reports, please check a [list of known issues](https://github.com/user-cont/colin/issues) to see
if the problem has already been reported (or fixed in a master branch).

If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/user-cont/colin/issues/new).
Be sure to include a **descriptive title and a clear description**. Ideally, please provide:
 * version of colin you are using (`rpm -q colin` or `pip3 freeze | grep colin`)
 * version of [conu](https://github.com/user-cont/conu) library (`rpm -q python3-conu` or `pip3 freeze | grep conu`)
 * version of [dockerfile-parse](https://github.com/DBuildService/dockerfile-parse) library (`rpm -q python3-dockerfile-parse` or `pip3 freeze | grep dockerfile-parse`)
 * version of container runtime you are using (`rpm -qa | grep docker`)
 * the command you executed, output and ideally please describe the image, container or dockerfile you are validating
   * invoke colin in debug mode (`--debug`)

If possible, add a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

**Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one. You can also comment on the closed issue to indicate that upstream should provide a new release with a fix.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.
When you are creating an enhancement issue, **use a clear and descriptive title**
and **provide a clear description of the suggested enhancement**
in as many details as possible.

## How to contribute code to colin

* Please make sure that your code complies with [PEP8](https://www.python.org/dev/peps/pep-0008/).
* One line should not contain more than 100 characters.
* Make sure that new code is covered by a test case (new or existing one).
* We don't like [spaghetti code](https://en.wikipedia.org/wiki/Spaghetti_code).
* The tests have to pass.

# How to write the new check to colin
All checks are stored in the directory
[checks](https://github.com/user-cont/colin/tree/master/colin/checks).
[Loader](https://github.com/user-cont/colin/tree/master/colin/core/loader.py)
obtains checks from there, and here's how:
 * classes which end with `AbstractCheck` are NOT loaded
 * only classes which with `Check` are loaded
 * the check class needs to be a child of a `AbstractCheck`

Here's a simple template how you can create a new check:

## Label check example
```python
from colin.core.checks.labels import LabelAbstractCheck


class FooBarLabelCheck(LabelAbstractCheck):
    name = "foobar_label"
    def __init__(self):
        super(self.__class__, self) \
                .__init__(
                        message="Label 'foobar' has to be specified.",
                        description="Provide a description for foobar label.",
                        reference_url="Specify URL to foobar reference",
                        tags=["foobar", "label"],
                        labels=["foobar"],
                        required=True,
                        value_regex=None
                )
```

Let's go through the list of keyword arguments:

- `name` — name of the check, this will be used to reference this check inside a ruleset.
- `message` — error message when the check fails.
- `description` gives information in colin's output on what this check does.
- `reference_url` — URL with even more info about the check. Ideally link to guidelines.
- `tags` — used to filter checks to run (`colin check -t foo` would run checks which have tag `foo`).
- `label` is a keyword argument specific to `LabelCheck` class.
- `required` — keyword specific to `LabelCheck` class. If the check fails and this is true, the check is marked as failed. If this is false and the check fails, it is a warning.

## File system check example
```python
from colin.core.checks.filesystem import FileCheck


class FooBarFileCheck(FileCheck):
    name = "foobar_file_required"
    def __init__(self):
        super(self.__class__, self) \
                .__init__(
                        message="The 'foobar' file has to be provided.",
                        description="This is a more detailed description",
                        reference_url="Reference to foobar file definition",
                        files=['/foobar'],
                        tags=['filesystem', 'foobar', 'banana'],
                        all_must_be_present=False
                )
```

We only need to describe one argument here:
- `files` is specific to `FileSystemCheck` class and indicates on what files we want to operate on.

## Add the new check into a ruleset
Once code for your check is complete, here's how you can run it.

Create a new ruleset file with your locally created check(s):  

```bash
$ cat foobar.yaml
version: '1'
checks:
- {name: foobar_label}
- {name: foobar_file_required}

```
__NOTE__: _Colin_ accepts `YAML` formatted ruleset files. As `JSON` is a subset of the `YAML` standard, `JSON` formatted
rulesets are also supported, but `YAML` is recommended.  

Then run it with colin using command:

```bash
$ python3 -m colin.cli.colin -f ./foobar.yaml <IMAGE-OR-DOCKERFILE>
```

The command above implies that your check lives happily with other checks in this upstream repo. It's possible to have checks stored externally and point colin to them.

Let's move one of the checks mentioned above to `/tmp/external_checks/checks.py`:
```
$ cat /tmp/external_checks/checks.py
from colin.core.checks.filesystem import FileCheck


class FooBarFileCheck(FileCheck):
    name = "foobar_file_required"
    def __init__(self):
        super(self.__class__, self) \
                .__init__(
                        message="The 'foobar' file has to be provided.",
                        description="This is a more detailed description",
                        reference_url="Reference to foobar file definition",
                        files=['/foobar'],
                        tags=['filesystem', 'foobar', 'banana'],
                        all_must_be_present=False
                )
```

This would be our simple ruleset:
```bash
$ cat foobar.json
{
    "version": "1",
    "checks": [{
        "name": "foobar_file_required"
    }]
}
```

And we would just call colin and point it to the directory containing python files with checks:
```
$ python3 -m colin.cli.colin -f ./foobar.json --checks-path /tmp/external_checks/ fedora:28
10:43:38.165 loader.py         DEBUG  Getting check(s) from the file '/tmp/external_checks/checks.py'.
10:43:38.165 loader.py         DEBUG  Will try to load selected file as module 'checks'.
10:43:38.168 ruleset.py        DEBUG  Check instance foobar_file_required added.
10:43:38.168 check_runner.py   DEBUG  Going through checks.
10:43:38.168 check_runner.py   DEBUG  Checking foobar_file_required
10:43:38.168 image.py          INFO   run container via binary in background
10:43:38.168 image.py          DEBUG  docker command: ['docker', 'run', '--entrypoint=', '-d', '--cidfile=/tmp/conu-91klvqm4/conu-vunlfypihipcrjesycltmmipcppeyrrq', '-l', 'conu.test_artifact', 'sha256:e555121ced0fcad9197d7d0445daff0e42d8f0e0c37362b66b817b8713dcbb3a', '/bin/sleep', 'infinity']
10:43:38.168 __init__.py       DEBUG  command: "docker run --entrypoint= -d --cidfile=/tmp/conu-91klvqm4/conu-vunlfypihipcrjesycltmmipcppeyrrq -l conu.test_artifact sha256:e555121ced0fcad9197d7d0445daff0e42d8f0e0c37362b66b817b8713dcbb3a /bin/sleep infinity"
fcd353d77b29323bdad64b555ac32405f663e45032e3c903da2888b8fd4d8304
10:43:39.237 probes.py         DEBUG  starting probe
10:43:39.240 probes.py         DEBUG  first process started: pid=19550
10:43:39.240 probes.py         DEBUG  pausing for 0.1 before next try
10:43:39.241 probes.py         DEBUG  Running "<lambda>" with parameters: "{}": 0/10
10:43:39.349 container.py      INFO   running command ['/bin/ls', '-1', '/foobar']
10:43:39.414 container.py      INFO   ls: cannot access '/foobar': No such file or directory
10:43:39.419 container.py      ERROR  command failed
10:43:39.419 container.py      INFO   exec metadata: {'ID': 'b8a20fd59296a650a31056fe9eed133d3d0610ffd258641f91070ddb46e06246', 'Running': False, 'ExitCode': 2, 'ProcessConfig': {'tty': False, 'entrypoint': '/bin/ls', 'arguments': ['-1', '/foobar'], 'privileged': False}, 'OpenStdin': False, 'OpenStderr': True, 'OpenStdout': True, 'CanRemove': False, 'ContainerID': 'fcd353d77b29323bdad64b555ac32405f663e45032e3c903da2888b8fd4d8304', 'DetachKeys': '', 'Pid': 19571}
10:43:39.419 filesystem.py     INFO   File /foobar is not present, ex: failed to execute command ['/bin/ls', '-1', '/foobar'], exit code 2
FAIL:The 'foobar' file has to be provided.

FAIL:1
```

Colin ships a set of predefined checks, which are available [in this
directory](https://github.com/user-cont/colin/tree/master/rulesets).

If your check is generic enough, it may make sense to add it to [default ruleset](https://github.com/user-cont/colin/blob/master/rulesets/default.json).


## Changelog

When you are contributing to changelog, please follow these suggestions:

* The changelog is meant to be read by everyone. Imagine that an average user
  will read it and should understand the changes. `Add check timeouts` is
  completely undescriptive.
* Every line should be a complete sentence. Either tell what is the change that the tool is doing or describe it precisely:
  * Bad: `Use search method in label regex`
  * Good: `Colin now uses search method when...`
* And finally, with the changelogs we are essentially selling our projects:
  think about a situation that you met someone at a conference and you are
  trying to convince the person to use the project and that the changelog
  should help with that.
