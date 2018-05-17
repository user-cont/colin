# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from colin.core.checks.cmd import CmdAbstractCheck


class ShellRunableCheck(CmdAbstractCheck):
    name = "shell_runnable"

    def __init__(self):
        super(ShellRunableCheck, self) \
            .__init__(message="Shell has to be runnable.",
                      description="The target has to be able to invoke shell.",
                      reference_url="https://docs.docker.com/engine/reference/run/",
                      tags=["sh", "cmd", "shell", "output"],
                      cmd=['sh', '-c', 'exit', '0'])
