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

from djamo import Document

from .base import Serializer


class EmbeddedDocument(Serializer):
    """
    This class represent a Mongodb embedded document. But only represent one
    document if you need a list of documents your should use this serializer
    with :py:class: `~djamo.serializers.List` serializer.

    :param document: Document class to embed.
    """

    def __init__(self, document, *args, **kwargs):
        self.document = document

    def validate(self, key, value):
        """
        Validate the ``value`` parameter against current serializer policy
        and riase
        :py:exception: `~djamo.serializers.Serializer.ValidationError`
        if value was not valid document subclass.
        """
        super(EmbeddedDocument, self).validate(key, value)
        if not isinstance(self.document(), Document):
            raise self.ValidationError(
                "'%s' should be a subclass of 'Document' class" % key)

    def serialize(self, value, **kwargs):
        """
        Serialize the given value.
        """
        return self.document(value).serialize()

    def deserialize(self, value):
        """
        De-serialize the given value
        """
        return self.document().deserialize(value)

    def is_valid_value(self, value):
        """
        Check the value against current serializer policy. The difference
        between this method and ``validate`` method is that this method
        just check value to possiblity of a valid value. But ``validate``
        check other parameter too like field requirement.
        """
        if isinstance(value, (self.document, dict)):
            return True

        return False
