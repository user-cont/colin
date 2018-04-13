from colin.checks.abstract.dockerfile import InstructionCheck


class FromTagCheck(InstructionCheck):

    def __init__(self):
        super().__init__(name="is_tag_not_latest",
                         message="",
                         description="",
                         reference_url="https://docs.docker.com/engine/reference/builder/#from",
                         tags=["from", "dockerfile", "latest"],
                         instruction="FROM",
                         value_regex=".*/latest$",
                         required=False)
    # TODO: Does not check if there is no tag => use ImageName parsing.
