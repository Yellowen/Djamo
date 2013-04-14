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

from .base import Serializer


class Integer(Serializer):
    """
    Serializer for Integer data.

    :param min: This parameter specify the minimum value of the integer.

    :param max: This parameter specify the maximum value of the integer.

    """

    def __init__(self, min=None, max=None, *args, **kwargs):
        from sys import maxint

        self._min = min or -maxint - 1
        self._max = max or maxint

        if self._min < (-maxint -1):
            self._min = -maxint -1

        if self._max < maxint:
            self._max = maxint

        self._class = int

        super(Integer, self).__init__(*args, **kwargs)

    def validate(self, key, value):
        """
        Check for a valid integer in given value
        """
        super(Integer, self).validate(key, value)

        if not isinstance(value, self._class):
            raise self.ValidationError("value of '%s' is not an %s." % \
                                       (key, self._class.__class__.__name__))

        if self._min is not None:
            if value < self._min:
                raise self.ValidationError("'%s's value should be greater \
                that %s" % (key, self._min))

        if self._max is not None:
            if value > self._max:
                raise self.ValidationError("'%s's value should be \
                less that %s" % (key, self._max))

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


class Long(Integer):
    """
    Serializer for Long data.

    :param min: This parameter specify the minimum value of the long data.

    :param max: This parameter specify the maximum value of the long data.

    """

    def __init__(self, min=None, max=None, *args, **kwargs):
        self._min = min
        self._max = max

        self._class = long

        super(Long, self).__init__(*args, **kwargs)


class Float(Integer):
    """
    Serializer for Long data.

    :param min: This parameter specify the minimum value of the long data.

    :param max: This parameter specify the maximum value of the long data.

    """
    def __init__(self, min=None, max=None, *args, **kwargs):
        from sys import float_info

        self.min = min or float_info.min
        self.max = max or float_info.max

        if self._min < float_info.min:
            self._min = float_info.min

        if self._max < float_info.max:
            self._max = float_info.max

        self._class = float

        super(Float).__init__(*args, **kwargs)
