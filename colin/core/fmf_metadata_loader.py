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

import os
import fmf

METADATA_LOCATION = os.path.dirname(__file__)

def get_fmf_from_class(obj):
    """
    transform class to parameteres for FMF
    :param obj: you can use then self.__class__
    :return: FMF tree item
    """
    if "." not in obj.__class__.__module__:
        modulename = obj.__class__.__module__
    else:
        modulename = obj.__class__.__module__.rsplit(".", 1)[1]
    modulename += ".py"
    filters = ["test:%s" % os.path.basename(modulename), "class:%s" % obj.__class__.__name__]
    return get_fmf_metadata(METADATA_LOCATION, filters=filters)


def get_fmf_metadata(fmfpath, keys=None, names=None, filters=None, object_list=False):
    """
    get fmf metadata for selected class, based on filters
    :param fmfpath:
    :param keys:
    :param names:
    :param filters:
    :param object_list:
    :return:
    """
    output = {}
    if keys is None:
        keys = []
    if names is None:
        names = []
    if filters is None:
        filters = []
    fmf_tree = fmf.Tree(fmfpath)
    items = [x for x in fmf_tree.prune(names=names, filters=filters, keys=keys) if x]
    if object_list:
        return items
    if len(items) == 1:
        output = items[0].data
    elif len(items) > 1:
        raise Exception("There is more FMF test metadata for item")
    return output


def set_fmf_metadata(target_object, metadata_dict):
    """
    set metadata to Object expected is any class derived from AbstractCheck
    :param target_object: any AbstractCheck derived class
    :param metadata_dict: values to set as instance variables
    :return: None
    """
    # set all attributes from FMF file as instance variables
    for k in metadata_dict:
        setattr(target_object, k, metadata_dict[k])
