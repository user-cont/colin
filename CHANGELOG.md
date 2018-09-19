# 0.2.0

* put output of atomic [un,]mount to logger, not colin's stdout
* Better name for the target.name property
* Use pytest coverage in CI as well
* Use target_type property for string representation of the target type
* Use coverage for tests
* Run tests on all target types
* Use name parameter for all targets
* Install xattr on ci setup
* Add setup for running in the CI
* Build the test-images only for integration tests
* Add docs and use better naming
* Use podman for the testing
* Use podman for image target
* Remove dockertar target
* Update docs
* Correct some other codacy warnings
* tests: compare dicts directly: pytest rocks
* Jirka loves dict comprehension
* correct grammar in an error message
* test properly usable_targets with different target types
* Allow release-bot to make PRs based on issues
* Readd readd
* Rename unused kwargs
* Resolve some codacy warnings
* Remove container target
* Optimize code format
* Optimize imports
* dont create pyc files when testing in container
* simplify image preparation, add target ostree
* pep8 fixes
* fixup: treat dockertars as images
* teach colin to accept docker image archives
* set fmf_metadata_path implicitly in case it is not set
* add missing dot
* fix issue caused by searching substrings for fmf metadata (now it search for endswith(/name))
* labels transformation to FMF format
* dynamic  checks metadata transform to FMF format
* deprecated labels transformation to FMF format
* bestpractices checks metadata transform to FMF format
* [README.md] Add build status badge
* allow to pull from insecure registries
* f: document the reason for atomic pull
* more helpful error message if the target can't be found
* cont: one func to run commands which logs well
* unmount mounted image during cleanup
* logging: do not readd handler if it's already there
* mk: add a way to run tests only
* nicer error message when an image can't be pulled
* address review from Dominika
* logging: default to WARN
* new cli arg: target type
* codacy fixes
* better debugging of atomic and skopeo
* check images without docker
* tests: bump dockerfile to F28
* Reverse the order of ruleset_dirs, i.e. Fix them.
* Correct order or dirs returned in get_rulesets_dir for correct "overwriting" scheme, as suggested by @lachmanfrantisek
* Nicer printing of list-rulesets
* list-rulesets prints full path to the ruleset files.
* Update ruleset getters so that it looks in all of the expected dirs
* Fix openshift labels in tests
* Changes as requested by @lachmanfrantisek and @TomasTomecek
* Fix maximum line-length issues in ruleset.py
* Update CONTRIBUTING.md mentioning YAML support.
* Update tests to go with PyYAML.
* Update helper ruleset functions to use YAML and JSON both.
* Update dependencies for PyYAML
* Use yaml.safe_load to deserialize ruleset files
* Check existence of json output file directory
* adapt PR review changes
* rename variable inside cycle
* remove io.openshift.tags check as well
* get just parameters from metadata what has to be used for class invocation
* remove io.o.expose-services
* simpler loading of checks
* contrib.md: fix examples, doc external checks
* --checks-path now accepts a list of paths
* tinker CONTRIBUTING.md
* set fmf metadata via loader.py to classes inherited from fmfabstractcheck
* changes based on PR review
* read fmf metadata for selected cases
* adapt PR review changes
* add checkpath option as cli option to specifi dir path to checks
* fix too long src line
* important fixes before FMF is adapted inside colin
* travis: require sudo b/c of sudo apt-...
* tests: more verbose logs
* enable all tests by default
* fix instruction checks when *_count is 0
* Correct description for the 'description_or_io.k8s.description_label' check
* Update config files from kwaciaren
* Correct the 'labels' attribute of the check
* Use bandit file from kwaciaren
* hi codacy
* error messages: grammar
* do not mount whole FS when checking for files
* move test images creation to conftest.py
* improve makefile, add there pip3 instead of pip and improve uninstall

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
