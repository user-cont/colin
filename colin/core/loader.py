import inspect

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

MODULE_NAME_IMPORTED_CHECKS = "colin.checks.imported"


def load_check_implementation(path):
    s = spec_from_file_location(MODULE_NAME_IMPORTED_CHECKS, path)
    m = module_from_spec(s)
    s.loader.exec_module(m)
    check_classes = []
    for name, obj in inspect.getmembers(m, inspect.isclass):
        if obj.__module__ == MODULE_NAME_IMPORTED_CHECKS:
            check_classes.append(obj())
    return check_classes
