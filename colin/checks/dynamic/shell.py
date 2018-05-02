from colin.checks.abstract.cmd import CmdCheck


class BashCheck(CmdCheck):

    def __init__(self):
        super(BashCheck, self) \
            .__init__(name="sh",
                      message="Shell has to be runnable.",
                      description="The target has to be able to invoke shell.",
                      reference_url="https://docs.docker.com/engine/reference/run/",
                      tags=["sh", "cmd", "shell", "output"],
                      cmd=['sh', '-c', 'exit', '0'])
