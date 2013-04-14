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

class Index(object):
    """
    This class represent a Mongodb collection Index. You must using it via
    :py:attribute: `~djamo.collection.BaseCollection.indexes` for example::

        class Students(Collection):

            indexes = [
                Index("name", unique=True),
                Index(["age", "uid"]),
            ]

    .. Note:: You can use Index separatly by using its ensure method.

    All optional index creation paramaters should be passed as keyword
    arguments to this method. Valid options include:

    * name: custom name to use for this index - if none is given,
            a name will be generated

    * unique: should this index guarantee uniqueness?

    * dropDups or drop_dups: should we drop duplicates

    * background: if this index should be created in the background
    * bucketSize or bucket_size: for use with geoHaystack indexes.
                                 Number of documents to group together
                                 within a certain proximity to a given
                                 longitude and latitude.

    * min: minimum value for keys in a GEO2D index
    * max: maximum value for keys in a GEO2D index
    * expireAfterSeconds: <int> Used to create an expiring (TTL) collection.
                          MongoDB will automatically delete documents from this
                          collection after <int> seconds. The indexed field
                          must be a UTC datetime or the data will not expire.

    :param keys: a single key or a list of (key, direction) pairs specifying
                 the index to create

    :param cache_time: (optional): time window (in seconds) during which this
                                   index will be recognized by subsequent calls
                                   to ``ensure_index`` - see documentation for
                                   ``ensure_index`` for details

    :param **kwargs: (optional): any additional index creation options (see
                     the above list) should be passed as keyword arguments.
    """
    def __init__(self, keys, cache_time=300, **kwargs):
        self.keys = keys
        self.cache_time = cache_time
        self.kwargs = kwargs

    def ensure(self, collection):
        """
        Create the index if it does not exists.

        :param collection: Collection object to create the index for.
        """
        return collection.ensure_index(self.keys,
                                       self.cache_time,
                                       **self.kwargs)
