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
import json

from six import iteritems
from colin.core.fmf_metadata_loader import get_fmf_from_class, set_fmf_metadata


class AbstractCheck(object):
    name = None
    message = ""
    description = ""
    reference_url = ""
    tags = []
    base_init_list = ["message", "description", "reference_url", "tags"]
    init_list = []

    def _meta_init(self, *args, **kwargs):
        """
        This method allows to use normal way via init parameters or alternative way of init via FMF format
        Default is to use args kwargs values, in case not given it tries to search for FMF metadata
        :param args:
        :param kwargs:
        :return:
        """
        required_value_list = list(set(self.base_init_list + self.init_list))
        if len(args) > 0 or len(kwargs) > 0:
            for cntr in range(len(args)):
                setattr(self, required_value_list[cntr], args[cntr])
            for v in kwargs:
                setattr(self, v, kwargs[v])
            for v in required_value_list:
                if not getattr(self, v):
                    raise ValueError("Missing option: %s" % v)
        else:
            fmfdata = get_fmf_from_class(self)
            if fmfdata:
                for v in required_value_list:
                    if v not in fmfdata:
                        raise ValueError("Missing option (FMF): %s" % v)
                set_fmf_metadata(self, fmfdata)

            else:
                raise Exception("no FMF metadata found for item", self, required_value_list, args, kwargs, fmfdata)


    def __init__(self, *args, **kwargs):
        self._meta_init(*args, **kwargs)

    def check(self, target):
        pass

    def __str__(self):
        return "{}\n" \
               "   -> {}\n" \
               "   -> {}\n" \
               "   -> {}\n" \
               "   -> {}\n".format(self.name,
                                   self.message,
                                   self.description,
                                   self.reference_url,
                                   ", ".join(self.tags))

    @property
    def json(self):
        """
        Get json representation of the check

        :return: dict (str -> obj)
        """
        return {
            'name': self.name,
            'message': self.message,
            'description': self.description,
            'reference_url': self.reference_url,
            'tags': self.tags,
        }

    @staticmethod
    def json_from_all_checks(checks):
        result_json = {}
        for (group, group_checks) in iteritems(checks):

            result_list = []
            for check in group_checks:
                result_list.append(check.json)

            result_json[group] = result_list
        return result_json

    @staticmethod
    def save_checks_to_json(file, checks):
        json.dump(obj=AbstractCheck.json_from_all_checks(checks=checks),
                  fp=file,
                  indent=4)
