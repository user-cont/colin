import click
from click.testing import CliRunner
from colin.cli.colin import check, list_checks, list_rulesets

def _call_colin(fnc):
    runner = CliRunner()
    return runner.invoke(fnc)

def test_check_command():
    result = _call_colin(check)
    expected_output = """Usage: check [OPTIONS] TARGET

Error: Missing argument "target".
"""
    assert result.exit_code == 2
    assert result.output == expected_output

def test_list_checks():
    result = _call_colin(list_checks)
    expected_output = """LABELS:
maintainer_label_required
   -> Label 'maintainer' has to be specified.
   -> The name and email of the maintainer (usually the submitter).
   -> https://fedoraproject.org/wiki/Container:Guidelines#LABELS
   -> ['maintainer', 'label', 'required']
   -> required

DOCKERFILE:
maintainer_deprecated
   -> 
   -> 
   -> https://docs.docker.com/engine/reference/builder/#maintainer-deprecated
   -> ['maintainer', 'dockerfile', 'deprecated']
   -> required

from_tag_not_latest
   -> In FROM, tag has to be specified and not 'latest'.
   -> Using the 'latest' tag may cause unpredictable builds.It is recommended that a specific tag is used in the FROM.
   -> https://fedoraproject.org/wiki/Container:Guidelines#FROM
   -> ['from', 'dockerfile', 'baseimage', 'latest']
   -> optional

"""
    assert result.exit_code == 0
    assert result.output == expected_output

def test_list_rulesets():
    result = _call_colin(list_rulesets)
    expected_output = """fedora
default
"""
    assert result.exit_code == 0
    assert result.output == expected_output
