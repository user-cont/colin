import os
import shutil

import colin.checks
from colin.core.loader import CheckLoader


def test_upstream_checks_can_be_loaded():
    """ check whether all upstream checks can be loaded """
    colin_checks_path = colin.checks.__file__
    colin_checks_dir = os.path.dirname(colin_checks_path)
    l = CheckLoader(colin_checks_dir)
    assert l.check_classes
    assert l.mapping["bzcomponent_deprecated"]


def test_loading_custom_check(tmpdir):
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    a_check_dir = os.path.join(tests_dir, "data", "a_check")
    shutil.copytree(a_check_dir, str(tmpdir.join("a_check")))
    l = CheckLoader(str(tmpdir))
    assert len(l.check_classes) == 2  # the check and abstract check
