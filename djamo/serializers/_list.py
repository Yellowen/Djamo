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


class List(Serializer):
    """
    Serializer for a list of data.
    """
    def __init__(self, data_type=None, *args, **kwargs):

        # TODO: Find a solution to suport multiple types
        self._type = data_type
        super(List, self).__init__(*args, **kwargs)

    def validate(self, key, value):
        """
        Validate the ``value`` parameter against current serializer policy
        and riase :py:exception: `~djamo.serializers.Serializer.ValidationError`
        if value was not valid.
        """
        super(List, self).validate(key, value)

        if not isinstance(value, (list, tuple)):
            raise self.ValidationError("'%s's value should be a instance of"
                                       "list or tuple." % key)

    def serialize(self, value, **kwargs):
        """
        Serialize the given value.
        """
        if self._type:
            return [self._type.serialize(i) for i in value]

        return value

    def deserialize(self, value):
        """
        De-serialize the given value
        """
        if self._type:
            return [self._type.deserialize(i) for i in value]

        return value

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        if isinstance(value, (tuple, list)):
            return True

        return False

# TODO: Add a Set serializer
