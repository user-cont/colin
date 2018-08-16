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

RULESET_DIRECTORY_NAME = "rulesets"
RULESET_DIRECTORY = "share/colin/" + RULESET_DIRECTORY_NAME
EXTS = [".yaml", '.yml', ".json"]

PASSED = "PASS"
FAILED = "FAIL"
ERROR = "ERROR"

COLOURS = {
    PASSED: "green",
    FAILED: "red",
    ERROR: "red"
}

OUTPUT_CHARS = {
    PASSED: ".",
    FAILED: "x",
    ERROR: "#"
}

COLIN_CHECKS_PATH = "CHECKS_PATH"
