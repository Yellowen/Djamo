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

from django.forms import Form

from djamo.utils import six
from djamo.options import Options


class DocumentFormMeta(type):
    """
    Meta class for DocumentForm object. This class is responsible for creating
    ``DocumentForm`` instances.

    .. Note:: This class is for Djamo internal usage.
    """

    def __new__(cls, name, bases, attrs):

        attr_meta = attrs.pop('Meta', None)
        new_class = type.__new__(cls, name, bases, attrs)

        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)

        else:
            meta = attr_meta

        if not hasattr(meta, "document"):
            raise AssertionError("No 'document' specified")

        setattr(new_class, "_meta", Options(meta))
        return new_class


class DocumentForm(six.with_metaclass(DocumentFormMeta, Form)):
    pass
