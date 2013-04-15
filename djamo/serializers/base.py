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
"""
All the serializers should be a subclass of the **Serializer** class.

.. NOTE: Since all the serializers are subclasses of the Serializer class
         all of them have the basic parameters of Serializer like ``required``
"""


class Serializer(object):
    """
    Base class for all the serializer classes. A serializer is a class that
    is responsible for serializing/de-serializing a value for an specific
    field of a document that specified by user in document class.

    :param required: If ``True`` the field is required and should have a value
                     in transaction time. default ``False``

    :param default: Default value of the field.
    """

    def __init__(self, required=False, default=None):
        self._required = required
        self._default = default

    def validate(self, key, value):
        """
        Validate the ``value`` parameter against current serializer policy
        and riase
        :py:exception: `~djamo.serializers.Serializer.ValidationError`
        if value was not valid.
        """
        if self._required and not value:
            raise self.ValidationError("'%s' field is required" % key)

    def serialize(self, value, **kwargs):
        """
        Serialize the given value.
        """
        return value

    def deserialize(self, value):
        """
        De-serialize the given value
        """
        return value

    @property
    def default_value(self):
        """
        The default value specified by user.
        """
        return self._default

    @property
    def is_required(self):
        """
        Return True if _required set to true.
        """
        return self._required

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        raise self.NotImplemented()

    class ValidationError(Exception):
        """
        This exception will raise in case of any validation problem.
        """
        pass

    class NotImplemented(Exception):
        """
        This exception will raise if any necessary methods does not
        override in subclasses.
        """
        pass
