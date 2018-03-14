from colin.checks.abstract.dockerfile import DockerfileCheck


class LayeredRunCheck(DockerfileCheck):

    def __init__(self):
        super().__init__(name="maintainer_deprecated",
                         message="",
                         description="",
                         reference_url="",
                         tags=["run", "dockerfile"]
                         )

    def check(self, target):
        pass
