import os

import pytest
from colin.core.ruleset.ruleset import Ruleset


def test_ruleset():
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    lol_ruleset_path = os.path.join(tests_dir, "data", "lol-ruleset.json")
    with open(lol_ruleset_path, "r") as fd:
        r = Ruleset(ruleset_file=fd)
        checks = r.get_checks(None)
    assert len(checks) == 1


def test_ruleset_tags():
    tags = ["a", "banana"]
    r = {
        "version": "1",
        "checks": [
            {
                "name": "name_label_required",
                "tags": tags.copy()
            }
        ]
    }
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    assert len(checks) == 1
    assert checks[0].tags == tags


def test_ruleset_additional_tags():
    tags = ["a"]
    r = {
        "version": "1",
        "checks": [
            {
                "name": "name_label_required",
                "additional_tags": tags.copy()
            }
        ]
    }
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    assert len(checks) == 1
    assert list(set(tags).intersection(set(checks[0].tags))) == tags


@pytest.mark.parametrize("tags,expected_check_name",[
    (["banana"], None),
    (["name"], "name_label_required")
])
def test_ruleset_tags_filtering(tags, expected_check_name):
    r = {
        "version": "1",
        "checks": [
            {
                "name": "name_label_required"
            }
        ]
    }
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None, tags=tags)
    if expected_check_name:
        assert len(checks) == 1
        assert checks[0].name == expected_check_name
    else:
        assert len(checks) == 0
