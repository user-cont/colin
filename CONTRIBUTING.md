# Contributing Guidelines

Thanks for your interest in contributing to `colin`.

The following is a set of guidelines for contributing to `colin`.
Use your best judgement, and feel free to propose changes to this document in a pull request.


## Reporting Bugs
Before creating bug reports, please check a [list of known issues](https://github.com/user-cont/colin/issues) to see
if the problem has already been reported (or fixed in a master branch).

If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/user-cont/colin/issues/new).
Be sure to include a **descriptive title and a clear description**. Ideally, please provide:
 * version of colin you are using (`rpm -q colin` or `pip freeze | grep colin`)
 * version of [conu](https://github.com/fedora-modularity/conu) library (`rpm -q python2-conu python3-conu` or `pip freeze | grep conu`)
 * version of [dockerfile-parse](https://github.com/DBuildService/dockerfile-parse) library (`rpm -q python2-dockerfile-parse python3-dockerfile-parse` or `pip freeze | grep dockerfile-parse`)
 * version of container runtime you are using (`rpm -qa | grep docker`)
 * the command you executed, output and ideally please describe the image, container or dockerfile you are validating
   * ideally, invoke colin in debug mode (`--debug`)

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
All checks are stored in the directory [checks](https://github.com/user-cont/colin/tree/master/colin/checks).
Think about what kind of check you would like to write and browse for already existing checks:
 - [best practices](https://github.com/user-cont/colin/tree/master/colin/checks/best_practices)
 - [containers](https://github.com/user-cont/colin/tree/master/colin/checks/containers)
 - [dockerfile](https://github.com/user-cont/colin/tree/master/colin/checks/dockerfile)
 - [images](https://github.com/user-cont/colin/tree/master/colin/checks/images)
 - [labels](https://github.com/user-cont/colin/tree/master/colin/checks/labels)

Here's a simple template how you can create a new check:

## Label check example
```python
from colin.checks.abstract.labels import LabelCheck

class FooBarLabelCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="foobar_label",
                      message="Label 'foobar' has to be specified.",
                      description="Provide a description for foobar label.",
                      reference_url="Specify URL to foobar reference",
                      tags=["foobar", "label"],
                      label="foobar",
                      required=True,
value_regex=None)
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
from colin.checks.abstract.filesystem import FileSystemCheck


class FooBarFileCheck(FileSystemCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="foobar_file_required",
                      message="The 'foobar' has to be provided.",
                      description="Just like traditional packages, containers need "
                                  "some 'man page' information about how they are to be used,"
                                  " configured, and integrated into a larger stack.",
                      reference_url="Reference to foobar file",
                      files=['/help.1'],
                      tags=['filesystem', 'helpfile', 'man'],
all_must_be_present=False)
```

We only need to describe one argument here:
- `files` is specific to `FileSystemCheck` class and indicates on what files we want to operate on.

## Add new check into relevant global configuration file
Once code for your check is complete, here's how you can run it.

First create a new ruleset file to test your check:
```bash
$ cat foobar.json
{
  "labels": {
    "required": [
      "foobar_label"
      ]
  }
}
```

And run it with colin using command:

```bash
$ python3 -m colin.cli.colin -f ./foobar.json <IMAGE-OR-DOCKERFILE>
```

The checks which are verified by colin are specified within ruleset files which
you find [in this
directory](https://github.com/user-cont/colin/tree/master/rulesets).

If your check is generic enough, it may make sense to add it to [default ruleset](https://github.com/user-cont/colin/blob/master/rulesets/default.json).


Thank you!
Colin team
