# Colin

Tool to check generic rules/best-practices for containers/images/dockerfiles.

Initial plan is to validate containers/images/dockerfiles against different ecosystems:
 - Red Hat Container Catalogue
 - Fedora Infra (and container guidelines)
 - CentOS
 - Atomic Container Best Practices

*Colin* will also provide generic checks for maintainers or users of containerized content.

![example](./docs/example.gif)

## Technical details

*Colin* will be available as a Python API, and will provide command line interface so you can easily use it locally.

Each ecosystem will define a set of checks to validate the artifacts. Checks will have different severity level so that we can classify checks as required or optional.

## TODO

- [ ] Provide cli.
- [ ] Implement basic checks.
- [ ] Packaging (pypi, rpm, ...)
