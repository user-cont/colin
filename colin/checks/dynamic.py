from colin.core.checks.cmd import CmdCheck


class ShellRunableCheck(CmdCheck):

    def __init__(self):
        super(ShellRunableCheck, self) \
            .__init__(name="shell_runnable",
                      message="Shell has to be runnable.",
                      description="The target has to be able to invoke shell.",
                      reference_url="https://docs.docker.com/engine/reference/run/",
                      tags=["sh", "cmd", "shell", "output"],
                      cmd=['sh', '-c', 'exit', '0'])
