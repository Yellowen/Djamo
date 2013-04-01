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

    def __init__(self):
        pass

    def validate(self, value):
        raise self.NotImplemented()

    def serialize(self, value):
        raise self.NotImplemented()

    def deserialize(self, value):
        raise self.NotImplemented()

    class NotImplemented(Exception):
        """
        This exception will raise by serializer if a required method not
        implemented in a serializer subclass.
        """
        pass
