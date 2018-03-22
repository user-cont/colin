from colin.checks.abstract.filesystem import FileSystemCheck


class HelpFileCheck(FileSystemCheck):

    def __init__(self):
        super().__init__(name="help_file_required",
                         message="The 'helpfile' has to be provided.",
                         description="Just like traditional packages, containers need "
                                     "some 'man page' information about how they are to be used,"
                                     " configured, and integrated into a larger stack.",
                         reference_url="https://fedoraproject.org/wiki/Container:Guidelines#Help_File",
                         files=['/help.1.', '/README.md'],
                         tags=['filesystem', 'helpfile', 'man'],
                         all_must_be_present=False)
