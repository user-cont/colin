# Colin

Tool to check generic rules/best-practices for containers/images/dockerfiles.

Initial plan is to validate containers/images/dockerfiles against different ecosystems:
 - Red Hat Container Catalogue
 - Fedora Infra (and container guidelines)
 - CentOS
 - Atomic Container Best Practices

*Colin* will also provide generic checks for maintainers or users of containerized content,


## Technical details

*Colin* will be available as a Python API, and the command line interface.

Each ecosystem defines set of checks for validation and their severity.
The check itself is a python class inherited from the abstract classes for each type of checks (dockerfile x image x container).


## TODO

- [ ] Provide cli.
- [ ] Implement basic checks.
- [ ] Packaging (pypi, rpm, ...)
