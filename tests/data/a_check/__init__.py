from colin.checks.abstract.abstract_check import AbstractCheck


class FunkyCheck(AbstractCheck):
    def __init__(self):
        super(FunkyCheck, self).__init__(
            name="this-is-funky-check",
            message="yes!",
            description="no",
            reference_url="https://nope.example.com/",
            tags=["yes", "and", "no"]
        )