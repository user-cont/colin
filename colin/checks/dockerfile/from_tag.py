from colin.checks.abstract.dockerfile import InstructionCheck


class FromTagCheck(InstructionCheck):

    def __init__(self):
        super().__init__(name="is_tag_latest",
                         message="",
                         description="",
                         reference_url="https://docs.docker.com/engine/reference/builder/#from",
                         tags=["from", "dockerfile", "latest"],
                         instruction="FROM",
                         regex=".*/latest$",
                         required=False)
