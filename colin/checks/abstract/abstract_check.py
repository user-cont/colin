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

class AbstractCheck(object):

    def __init__(self, name, message, description, reference_url, tags):
        super().__init__()
        self.name = name
        self.message = message
        self.description = description
        self.reference_url = reference_url
        self.tags = tags
        self.severity = None

    def check(self, target):
        pass
