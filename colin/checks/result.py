import json

from six import itervalues, iteritems

from ..core.constant import REQUIRED, PASSED, FAILED, WARNING, OPTIONAL


class AbstractResult(object):

    def __init__(self, ok, description, message, reference_url, check_name, severity):
        super().__init__()
        self.ok = ok
        self.description = description
        self.message = message
        self.reference_url = reference_url
        self.check_name = check_name
        self.severity = severity

    @property
    def status(self):
        statuses = {REQUIRED: (PASSED, FAILED),
                    OPTIONAL: (PASSED, WARNING)}
        status_ok, status_nok = statuses[self.severity]

        return status_ok if self.ok else status_nok

    def __str__(self):
        return "{}:{}:{}".format("ok " if self.ok else "nok",
                                 self.status,
                                 self.check_name)


class DockerfileCheckResult(AbstractResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, lines=None,
                 correction_diff=None):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.lines = lines
        self.correction_diff = correction_diff


class ContainerCheckResult(AbstractResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, logs):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.logs = logs


class ImageCheckResult(AbstractResult):

    def __init__(self, ok, description, message, reference_url, check_name, severity, logs):
        super().__init__(ok, description, message, reference_url, check_name, severity)
        self.logs = logs


class CheckResults(object):

    def __init__(self, results):
        self._results = results
        self._generated = False
        self._generated_result = {}

    @property
    def _dict_of_results(self):
        result_json = {}
        for group, results in self.results:
            result_list = []
            for r in results:
                result_list.append({
                    'name': r.check_name,
                    'ok': r.ok,
                    'status': r.status,
                    'description': r.description,
                    'message': r.message,
                    'reference_url': r.reference_url,
                    'severity': r.severity
                })
            result_json[group] = result_list
        return result_json

    @property
    def json(self):
        return json.dumps(self._dict_of_results, indent=4)

    @property
    def all_results(self):
        result = []
        for _, checks in self.results:
            result += checks
        return result

    def save_json_to_file(self, file):
        json.dump(obj=self._dict_of_results,
                  fp=file,
                  indent=4)

    @property
    def results(self):
        if self._generated:
            return iteritems(self._generated_result)
        else:
            return self._group_generator()

    def _group_generator(self):
        for group, group_result in self._results:
            self._generated_result.setdefault(group, [])
            yield group, self._result_generator(group=group,
                                                results=group_result)
        self._generated = True

    def _result_generator(self, group, results):
        for r in results:
            self._generated_result[group].append(r)
            yield r
