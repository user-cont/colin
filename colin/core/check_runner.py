from six import iteritems

from ..checks.result import CheckResults


def go_through_checks(target, checks):
    results = _group_generator(target=target,
                               checks=checks)
    return CheckResults(results=results)


def _result_generator(target, checks):
    for check in checks:
        yield check.check(target)


def _group_generator(target, checks):
    for (group, group_checks) in iteritems(checks):
        yield group, _result_generator(target=target,
                                       checks=group_checks)
