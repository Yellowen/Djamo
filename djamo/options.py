# -----------------------------------------------------------------------------
#    Djamo - Yetanother Mongodb driver for Django
#    Copyright (C) 2012-2013 Yellowen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------
from djamo.utils import six


class Options(object):
    """
    This class represent options used any where.
    """
    app_label = ""
    verbose_name = ""
    verbose_name_plural = ""
    document_name = ""
    attributes = {}
    document = ""
    include = []
    exclude = []

    def __init__(self, meta, **kwargs):

        for key, value in six.iteritems(kwargs):
            self.set_attr(key, value)

        if meta:
            for key, value in  six.iteritems(meta.__dict__):
                self.set_attr(key, value)

    def set_attr(self, key, value):
        my_attr = getattr(self, key, None)
        if my_attr is not None:
            setattr(self, key, value)
