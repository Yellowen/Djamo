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

from .base import Serializer


class String(Serializer):
    """
    Serializer for string data.

    :param min_length: This parameter specify the minimum length of the string.

    :param max_length: This parameter specify the maximum length of the string.
    """

    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        self._min = min_length
        self._max = max_length

        super(String, self).__init__(*args, **kwargs)

    def validate(self, key, value):
        """
        Check for a valid string in given value
        """
        super(String, self).validate(key, value)

        self.u(value)

        if self._min is not None:
            if len(value) < self._min:
                raise self.ValidationError(
                    "Length of '%s's value should be more" \
                    "that %s character" % (key, self._min))

        if self._max:
            if len(value) > self._max:
                raise self.ValidationError("Length of '%s's value should be" \
                "less that %s character""" % (key, self._max))

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        if isinstance(value, six.string_types):
            return True

        return False

    def serialize(self, value, **kwargs):
        """
        Serialize the given value.
        """
        return six.u(value)

    def deserialize(self, value):
        """
        De-serialize the given value
        """
        return self.u(value)

    def u(self, value):
        """
        cast the given value to unicode

        """
        if six.PY3:
            return value
        else:

            if isinstance(value, str):
                return unicode(value)

            elif isinstance(value, unicode):
                return value

            else:
                return six.u(value)
