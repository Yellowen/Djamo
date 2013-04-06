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


class Serializer(object):
    """
    Base class for all the serializer classes.
    """

    def __init__(self, required=False, default=None):
        self._required = required
        self._default = default

    def validate(self, value):
        if self._required and not value:

            # TODO: Use a 'key' in the exception.
            raise self.ValidationError("This field is required")

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    @property
    def default_value(self):
        return self._default

    class ValidationError(Exception):
        """
        This exception will raise in case of any validation problem.
        """
        pass
