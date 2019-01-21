# 0.3.1

## Fixes

- Fix metadata checks (ENV, USER) for podman images.
- Fix Fedora packaging. (Conu was temporarily removed from requirements.)
- Documentation updated.

## Breaking changes

* Remove support for Python 2.


# 0.3.0

## New Features

* You can configure timeout for checks now:
  * This can be done via CLI or add `timeout: <seconds>` to a check in a ruleset.
  * Default timeout is set to 10 minutes.
* Checks can be skipped via CLI option `--skip`.

## Breaking changes

* Colin searches a value in label now instead of matching it using a regex.

## Fixes

* Output a sensible error message when the check code cannot be found.
* Handle the situation when the instruction FROM is missing in testing image tag.


# 0.2.1

## New Features

* Allow setting CLI options via environment variables
* Allow loading rulesets from virtualenv
* Add info subcommand

# 0.2.0

## Breaking changes

* switch from docker to podman, thanks to @lachmanfrantisek
* remove `container` target type
* new cli arg: target type (defaults to image -- for podman)

## New Features

* add `ostree` target, thanks to @TomasTomecek
* use fmf format in checks, thanks to @jscotka
* allow rulesets in the YAML format, thanks to @SkullTech

## Fixes

* many code style fixes
* use Centos CI, thanks to @jpopelka
* better loading of the ruleset files (subdir -> user -> system), thanks to @SkullTech
* check existence of json output file directory
* simpler loading of checks
* tinker CONTRIBUTING.md
* do not mount whole FS when checking for files
* improve tests quality


# 0.1.0

Welcome to the first official release of colin. With `0.0.*` releases we tried to iterate on a minimal viable product and with this `0.1.0` release we believe it's finally here.

# Features

* Validate a selected artifact against a ruleset.
* Artifacts can be container images, containers and dockerfiles.
* We provide a default ruleset we believe every container should satisfy.
* There is a ruleset to validate an artifact whether it complies to [Fedora Container Guidelines](https://fedoraproject.org/wiki/Container:Guidelines)
* Colin can list available rulesets and list checks in a ruleset.
* There is a python API available
* Colin can be integrated into your workflow easily - it can provide results in json format.
