# Contributing Guidelines

Thanks for interest in contribution to `colin`.

The following is a set of guidelines for contributing to `colin`. These are not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## How to contribute to colin

### Reporting Bugs
Before creating bug reports, please check a [list of known issues](https://github.com/user-cont/colin/issues) to see
if the problem has already been reported.

If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/user-cont/colin/issues/new).
Be sure to include a **descriptive title, clear description and a package version** and please include **as many details as possible** to help maintainers reproduce
the issue and resolve it faster.
If possible, add a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

## How to write the new check to colin
All checks are stored in the directory [checks](https://github.com/user-cont/colin/tree/master/colin/checks).
Think about what kind of check you would like to write and browse for already existing checks:
 - [best practices](https://github.com/user-cont/colin/tree/master/colin/checks/best_practices)
 - [containers](https://github.com/user-cont/colin/tree/master/colin/checks/containers)
 - [dockerfile](https://github.com/user-cont/colin/tree/master/colin/checks/dockerfile)
 - [images](https://github.com/user-cont/colin/tree/master/colin/checks/images)
 - [labels](https://github.com/user-cont/colin/tree/master/colin/checks/labels)

If you observe, that check is missing, write the new one in python which will follow this template, e.g.

### Label check example
```bash
from colin.checks.abstract.labels import LabelCheck

class FooBarLabelCheck(LabelCheck):

    def __init__(self):
        super(self.__class__, self) \
            .__init__(name="foobar_label",
                      message="Label 'foobar' has to be specified.",
                      description="Provide a description for foobar label.",
                      reference_url="Specify URL to foobar reference",
                      tags=["foobar", "label", "required"],
                      label="foobar",
                      required=True,
value_regex=None)
```

### File system check example
```bash
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

### Add new check into relevant global configuration file
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