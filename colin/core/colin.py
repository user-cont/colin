from colin.core.check_runner import go_through_checks
from colin.core.config.config import Config
from colin.core.target import CheckingTarget


def run(name_of_target, group=None, severity=None, tags=None, config_name=None):
    target = CheckingTarget(name=name_of_target)
    config = Config(name=config_name)
    checks_to_run = config.get_checks(group=group,
                                      severity=severity,
                                      tags=tags,
                                      target_type=target.target_type)
    result = go_through_checks(object_to_check=target,
                               checks=checks_to_run)
    return result
