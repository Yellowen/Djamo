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


class Integer(Serializer):
    """
    Serializer for Integer data.

    :param min_value: This parameter specify the minimum value of the integer.

    :param max_value: This parameter specify the maximum value of the integer.

    """

    def __init__(self, min_value=None, max_value=None,
                 klass=int, *args, **kwargs):
        try:
            from sys import maxint
            MAXSIZE = maxint
        except ImportError:
            MAXSIZE = six.MAXSIZE

        self._min = min_value or -MAXSIZE - 1
        self._max = max_value or MAXSIZE

        if self._min < (-MAXSIZE - 1):
            self._min = -MAXSIZE - 1

        if self._max > MAXSIZE:
            self._max = MAXSIZE

        self._class = klass

        super(Integer, self).__init__(*args, **kwargs)

    def validate(self, key, value):
        """
        Check for a valid integer in given value
        """
        super(Integer, self).validate(key, value)

        try:
            self._class(value)
        except ValueError:
            raise self.ValidationError("'%s's value should be an instance"
                                       "of %s" % (key, self._class))
        if self._min is not None:
            if value < self._min:
                raise self.ValidationError("'%s's value should be greater "
                "that %s" % (key, self._min))

        if self._max is not None:
            if value > self._max:
                raise self.ValidationError("'%s's value should be "
                "less that %s" % (key, self._max))

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        if isinstance(value, self._class):
            return True

        return False

    def serialize(self, value, **kwargs):
        """
        Serialize the given value.
        """
        return self._class(value)

    def deserialize(self, value):
        """
        De-serialize the given value
        """
        return self._class(value)


class Float(Integer):
    """
    Serializer for Long data.

    :param min_value: This parameter specify the minimum value of the long
                      data.

    :param max_value: This parameter specify the maximum value of the long
                      data.

    """
    def __init__(self, min_value=None, max_value=None,
                 required=False, default=None,
                 *args, **kwargs):

        from sys import float_info

        self._min = min_value or float_info.min
        self._max = max_value or float_info.max
        self._required = required
        self._default = default

        if self._min < float_info.min:
            self._min = float_info.min

        if self._max > float_info.max:
            self._max = float_info.max

        self._class = float
