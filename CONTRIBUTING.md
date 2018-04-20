# Contributing Guidelines

Thanks for interest in contribution to `colin`.

The following is a set of guidelines for contributing to `colin`.
Use your best judgment, and feel free to propose changes to this document in a pull request.

## How to contribute code to colin

### Reporting Bugs
Before creating bug reports, please check a [list of known issues](https://github.com/user-cont/colin/issues) to see
if the problem has already been reported.

If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/user-cont/colin/issues/new).
Be sure to include a **descriptive title, clear description and a package version** and please include **as many details as possible** to help maintainers reproduce
the issue and resolve it faster.
If possible, add a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.
When you are creating an enhancement issue, **use a clear and descriptive title**
and **provide a clear description of the suggested enhancement**
in as many details as possible.

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

- `name` means what kind label we check. It has to end with `_label`.
- `message` is shows in case check is not fulfilled.
- `description` provides information, why the check has to be specified.
- `reference_url` references to an URL for specific check.
- `tags`
- `label` means name of the label, that will be checked.
- `required` specifies label has to be present. Otherwise label is not allowed (e.g. deprecated label).
- `value_regex` means regular expression to check label.

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
- `files` means what kind of files are checked in an image.

The rest are the same as in LabelCheck example.

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

And run it with colin, by a command:

```bash
$ python3 -m colin.cli.colin -f ./foobar.json fedora:27
```

The checks which are verified by colin are specified
in the [ruleset](https://github.com/user-cont/colin/tree/master/rulesets) directory.
Add your new check into [default.json](https://github.com/user-cont/colin/blob/master/rulesets/default.json) or
[fedora.json](https://github.com/user-cont/colin/blob/master/rulesets/fedora.json.
E.g. Fedora required labels have to be added into this dictionary:

```bash
 "labels": {
    "required": [
      "maintainer",
      "name",
```

Thank you!
Colin team