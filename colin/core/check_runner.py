from colin.checks.result import CheckResults


def go_through_checks(target, checks):
    results = []
    for check in checks:
        results.append(check.check(target))
    return CheckResults(results=results)
