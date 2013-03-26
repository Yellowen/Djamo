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
from pymongo.collection import Collection as MongoCollection


class Collection (MongoCollection):
    """
    Djamo implementation of Mongodb collection.
    """

    #: Class that will be use to as a document class for this collection
    document = None

    #: Specify the name of collection in database level. In case of a None
    #: value current collection class name will use in lower case
    name = None

    def __init__(self, create=False, *args, **kwargs):
        from djamo.db import client

        self.name = self.name or self.__class__.__name__.lower()
        self.db = client.get_database()

        super(Collection, self).__init__(self.db, self.name, create,
                                         *args, **kwargs)
