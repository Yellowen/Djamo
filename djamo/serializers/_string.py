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


class String(Serializer):
    """
    Serializer for string data.

    :param required: If ``True`` the field is required and should have a value
                     in transaction time. default ``False``

    :param default: Default value of the field.
    """

    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        self._min = min_length or 0;
        self._max = max_length

        super(String, self).__init__(*args, **kwargs)

    def validate(self, key, value):
        """
        Check for a valid string in given value
        """
        super(String, self).validate(value)

        if not isinstance(value, basestring):
            raise self.ValidationError("value of '%s' is not an string." % key)

        if len(value) < self._min:
            raise self.ValidationError("Length of '%s's value should be more \
            that %s character" % (key, self._min))

        if self._max:
            if len(value) > self._max:
                raise self.ValidationError("Length of '%s's value should be \
                less that %s character" % (key, self._max))

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        if isinstance(value, basestring):
            return True

        return False
